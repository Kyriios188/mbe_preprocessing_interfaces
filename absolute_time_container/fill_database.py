import os
import datetime

from database import Step, Experiment, OtherStep, Layer

folderpath = 'files/'


def fill_database():
    filename: str = os.listdir(folderpath)[0]

    with open(file=folderpath+filename, mode='r', encoding='utf-8', errors='replace') as f:


        # The log files are small (<100 lines) and their size is proportional to the number of Layers,
        # so we can afford to open them multiple times.
        experiment: Experiment = Experiment(
            log_file_name=filename,
            experiment_keyword='Bragg',  # TODO: should be given by app.py through the request
            file_path=folderpath+filename
        )
        previous_step: Step

        all_lines = f.readlines()
        found_start = False
        found_end = False

        for i, line in enumerate(all_lines):

            lower_line: str = line.lower()
            line_type: str = Step.identify_line(lower_line)
            current_step_number: int = Step.get_step_number(lower_line)

            if (not found_start and line_type != 'start') or found_end or line_type == 'loop':
                continue

            line_timestamp: datetime.datetime = Step.get_timestamp(line)

            # If there is no previous_step
            if line_type == 'start':
                experiment.init_time = line_timestamp
                found_start = True
                previous_step = OtherStep(
                    experiment=experiment,
                    line=line,
                    line_index=i,
                    line_type=line_type,
                )

            # If this is the last step i.e. the step before the ------> Stopped/Completed
            elif current_step_number == experiment.last_step_number:
                # Finish the last step
                found_end = True
                previous_step.end = line_timestamp
                experiment.step_list.append(previous_step)

                last_step = OtherStep(
                    experiment=experiment,
                    line=line,
                    line_index=i,
                    line_type=line_type
                )
                last_step.end = line_timestamp  # This step starts and finishes instantly
                experiment.end_time = line_timestamp
                experiment.step_list.append(last_step)
                

            # If there is a previous_step from past loop and if it is not the final line in the file
            else:
                # Finish previous step
                previous_step.end = line_timestamp
                experiment.step_list.append(previous_step)

                # initialize next step
                if line_type == 'layer':
                    previous_step = Layer(
                        experiment=experiment,
                        line=line,
                        line_index=i
                    )
                    experiment.n_layers += 1
                else:
                    previous_step = OtherStep(
                        experiment=experiment,
                        line=line,
                        line_index=i,
                        line_type=line_type
                    )
    return experiment