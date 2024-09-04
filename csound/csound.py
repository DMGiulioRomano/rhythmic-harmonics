import os
import sys
import configparser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pyLib')))
from markdown_utils import read_markdown_file, filter_comments, parse_line, Voce

# ---------------------------------------------------------------
# Define default values
COLOR_TO_SOUND_FILE = {}
poly = False
duration0thHarmonics = 7.0
# ---------------------------------------------------------------

def load_config(config_file):
    global COLOR_TO_SOUND_FILE, poly, duration0thHarmonics
    config = configparser.ConfigParser()
    config.read(config_file)
    # Load sound files
    color_to_sound_file = config['SoundFiles']
    for key, value in color_to_sound_file.items():
        file_path, max_duration = value.split(', ')
        COLOR_TO_SOUND_FILE[key] = [file_path, float(max_duration)]
    # Load parameters
    poly = config.getboolean('Parameters', 'poly')
    duration0thHarmonics = config.getfloat('Parameters', 'duration0thHarmonics')



class TimeOrchestrator:
    def __init__(self, LengthLineSec):
        self.LengthLineSec = LengthLineSec
    
    def calculate_at(self, x, y, z):
        return (x * self.LengthLineSec) + ((self.LengthLineSec / y) * z)

class Evento:
    def __init__(self, at, sound_file='default.wav', max_dur=.1, dur=1):
        self.at = at
        self.dur = dur
        self.sound_file = sound_file
        self.max_dur = max_dur

    def to_csound(self):
        return f'i1 {self.at} {self.dur} "{self.sound_file}"\n'

def parse_input_line(line, orchestrator):
    try:
        parsed_data = parse_line(line)
        if parsed_data:
            x, y, z, _ = parsed_data
            color_code = line.split()[-1]
            sound_file, max_duration = COLOR_TO_SOUND_FILE.get(color_code, [COLOR_TO_SOUND_FILE.get('0')[0], COLOR_TO_SOUND_FILE.get('0')[1]])
            at = orchestrator.calculate_at(x, y, z)
            return Evento(at, sound_file=sound_file, max_dur=max_duration), color_code
    except Exception as e:
        print(f"Error parsing line '{line}': {e}")
    return None, None

def process_markdown(input_file, orchestrator, poly):
    eventi = []
    lines = read_markdown_file(input_file)
    filtered_lines = filter_comments(lines)
    
    for line in filtered_lines:
        evento, color_code = parse_input_line(line, orchestrator)
        if evento:
            eventi.append((evento, color_code))
    
        # Sort points based on the 'at' attribute
    sorted_eventi = sorted(eventi, key=lambda e: e[0].at)

    if not poly:
        for i in range(len(sorted_eventi) - 1):
            next_at = sorted_eventi[i + 1][0].at
            max_duration = sorted_eventi[i][0].max_dur
            sorted_eventi[i][0].dur = max(next_at - sorted_eventi[i][0].at, max_duration)
        
        if sorted_eventi:
            sorted_eventi[-1][0].dur = 1.0
    else:
        for evento, _ in sorted_eventi:
            evento.dur = evento.max_dur

    return sorted_eventi

def write_csound_output(eventi, output_file):
    with open(output_file, 'w') as cs_file:
        cs_file.write(";< Csound Score File >\n")
        
        # Group events by color code
        voci = {}
        for evento, color_code in eventi:
            if color_code not in voci:
                voci[color_code] = Voce(color_code)
            voci[color_code].add_point(evento)

        # Write the events for each voice
        for color, voce in voci.items():
            # Write a comment for each voice
            cs_file.write(f'; Voice for color code: {color}\n')
            for evento in voce.punti:
                cs_file.write(evento.to_csound())
        
        # End of the score
        cs_file.write("e\n")  # End of the score event

if __name__ == "__main__":
    config_file = '../config.ini'  # Name of the config file
    input_markdown = "../input.md"  # Name of the input markdown file
    output_csound = "eventi.sco"  # Name of the Csound output file
    
    # Load the configuration
    load_config(config_file)
    
    # Create the orchestrator with a specified LengthLineSec
    orchestrator = TimeOrchestrator(LengthLineSec=duration0thHarmonics)  # Use the defined duration0thHarmonics

    # Process the markdown file and write the Csound output
    eventi = process_markdown(input_markdown, orchestrator, poly)
    write_csound_output(eventi, output_csound)
