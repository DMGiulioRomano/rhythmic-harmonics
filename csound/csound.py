# ---------------------------------------------------------------
#                           PARAMETERS
# Define the sound file dictionary with lists containing the sound file and the max duration
COLOR_TO_SOUND_FILE = {
    '0': ['../rec/1.wav', 0.4],  # File and maximum duration
    '1': ['../rec/2.wav', 1.0],  # File and maximum duration
    # Add more mappings if needed
}
# Boolean to decide whether to calculate durations based on the minimum of max duration and difference in 'at'
poly = False  # Set to True if you want the duration to be the minimum of max duration and difference in 'at'
# Define the length of the line in seconds
duration0thHarmonics = 7.0
# ---------------------------------------------------------------








class TimeOrchestrator:
    def __init__(self, LengthLineSec):
        """
        Initializes a TimeOrchestrator object.

        Args:
        LengthLineSec (float): The length in seconds of a line.
        """
        self.LengthLineSec = LengthLineSec
    
    def calculate_at(self, x, y, z):
        """
        Calculate the 'at' value for an event based on the input parameters.

        Args:
        x (int): The first numerical component of the input line.
        y (int): The second numerical component of the input line.
        z (int): The third numerical component of the input line.

        Returns:
        float: The calculated 'at' value.
        """
        return (x * self.LengthLineSec) + ((self.LengthLineSec / y) * z)


class Evento:
    def __init__(self, at, sound_file='default.wav',max_dur=.1, dur=1):
        """
        Initializes an Evento object with the specified parameters.

        Args:
        at (float): Time at which the event starts.
        sound_file (str): Sound file associated with the event, default is 'default.wav'.
        dur (float): Duration of the event, default is 1.
        """
        self.at = at
        self.dur = dur  # Duration of the event
        self.sound_file = sound_file  # Sound file associated with the event
        self.max_dur = max_dur

    def to_csound(self):
        """
        Convert the event to a Csound score line.

        Returns:
        str: The Csound score line representation of the event.
        """
        return f'i1 {self.at} {self.dur} "{self.sound_file}"\n'


def parse_input_line(line, orchestrator):
    try:
        # Split the line into components
        parts = line.split()
        if len(parts) < 2:
            raise ValueError("Invalid format: At least one space-separated value is required after the '-'.")
        
        # Extract the main part and sound file part
        event_part, color_code = ' '.join(parts[:-1]), parts[-1]
        sound_file, max_duration = COLOR_TO_SOUND_FILE.get(color_code, [COLOR_TO_SOUND_FILE.get('0')[0],COLOR_TO_SOUND_FILE.get('0')[1]])
        
        # Further split the event part
        x, y, z = map(int, event_part.split('-'))
        
        # Calculate 'at' using the orchestrator
        at = orchestrator.calculate_at(x, y, z)

        return Evento(at, sound_file=sound_file, max_dur=max_duration)

    except ValueError as e:
        print(f"Error: {e}")
        return None


def process_markdown(input_file, orchestrator, poly):
    eventi = []
    with open(input_file, 'r') as md_file:
        for line in md_file:
            line = line.strip()
            if line:  # If the line is not empty
                evento = parse_input_line(line, orchestrator)
                if evento:
                    eventi.append(evento)
    
    if not poly:
        # Calculate the duration of each event as the minimum between the max duration and the difference in 'at' value
        for i in range(len(eventi) - 1):
            next_at = eventi[i + 1].at
            max_duration = eventi[i].max_dur
            eventi[i].dur = max(next_at - eventi[i].at, max_duration)
        
        # The last event can have a default duration, e.g., 1 second
        if eventi:
            eventi[-1].dur = 1.0
    else:
        # If poly is False, set the duration to the max duration from the dictionary
        for evento in eventi:
            evento.dur = evento.max_dur

    return eventi


def write_csound_output(eventi, output_file):
    with open(output_file, 'w') as cs_file:
        for evento in eventi:
            cs_file.write(evento.to_csound())


if __name__ == "__main__":
    input_markdown = "../input.md"  # Name of the input markdown file
    output_csound = "eventi.sco"  # Name of the Csound output file
    
    # Create the orchestrator with a specified LengthLineSec
    orchestrator = TimeOrchestrator(LengthLineSec=duration0thHarmonics)  # Use the defined duration0thHarmonics

    eventi = process_markdown(input_markdown, orchestrator, poly)
    write_csound_output(eventi, output_csound)
