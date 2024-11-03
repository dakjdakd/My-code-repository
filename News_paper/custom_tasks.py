from crewai import Task

class AppendTask(Task):
    def _save_output(self, output: str):
        """Override to append to the output file instead of overwriting."""
        if self.output_file:
            with open(self.output_file, "a", encoding="utf-8") as file:
                file.write(output)
                file.write("\n")