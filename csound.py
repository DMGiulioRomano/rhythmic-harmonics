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
    def __init__(self, at, dur=1):
        """
        Initializes a Evento object with the specified parameters.

        Args:
        at (float): Time at which the event starts.
        dur (float): Duration of the event, default is 1.
        """
        self.at = at
        self.dur = dur  # Duration of the event

    def to_csound(self):
        """
        Convert the event to a Csound score line.

        Returns:
        str: The Csound score line representation of the event.
        """
        return f"i1 {self.at} {self.dur}\n"


def parse_input_line(line, orchestrator):
    try:
        # Dividi la riga in tre componenti
        x, y, z = map(int, line.split('-'))
        
        # Calcola 'at' utilizzando l'orchestrator
        at = orchestrator.calculate_at(x, y, z)

        return Evento(at)

    except ValueError as e:
        print(f"Errore: {e}")
        return None


def process_markdown(input_file, orchestrator, calculate_durations):
    eventi = []
    with open(input_file, 'r') as md_file:
        for line in md_file:
            line = line.strip()
            if line:  # Se la riga non è vuota
                evento = parse_input_line(line, orchestrator)
                if evento:
                    eventi.append(evento)
    
    if calculate_durations:
        # Calcola la durata di ogni evento come differenza tra at successivo e at corrente
        for i in range(len(eventi) - 1):
            eventi[i].dur = eventi[i + 1].at - eventi[i].at
        
        # L'ultimo evento può avere una durata predefinita, ad esempio 1 secondo
        if eventi:
            eventi[-1].dur = 1.0
    else:
        # Se la durata non deve essere calcolata, la impostiamo a 1 per tutti
        for evento in eventi:
            evento.dur = 1.0

    return eventi


def write_csound_output(eventi, output_file):
    with open(output_file, 'w') as cs_file:
        for evento in eventi:
            cs_file.write(evento.to_csound())


if __name__ == "__main__":
    input_markdown = "input.md"  # Nome del file markdown di input
    output_csound = "eventi.sco"  # Nome del file di output Csound
    
    # Creazione dell'orchestratore con una LengthLineSec specificata
    orchestrator = TimeOrchestrator(LengthLineSec=10.0)  # Puoi cambiare il valore di LengthLineSec

    # Booleano per decidere se calcolare le durate dinamicamente o fissarle a 1
    calculate_durations = False  # Imposta a False se vuoi che la durata sia sempre 1

    eventi = process_markdown(input_markdown, orchestrator, calculate_durations)
    write_csound_output(eventi, output_csound)
