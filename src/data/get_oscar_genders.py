import pandas as pd
import tqdm
import json
from openai import OpenAI


class OscarDataProcessor:
    def __init__(self, api_key: str, input_file: str, batch_size: int = 5):
        self.api_key = api_key
        self.input_file = input_file
        self.batch_size = batch_size
        self.oscar_award = None
        self.genders = []
        self.prompt_to_response_cache = []
        self.client = OpenAI(api_key=self.api_key)

    def load_data(self):
        """ Load the Oscar award data from the CSV file. """
        print(f"Loading data from {self.input_file}...")
        self.oscar_award = pd.read_csv(self.input_file)

    def ask_openai(self, prompt: str) -> str:
        """ Query the OpenAI model with a given prompt. """
        print("Sending prompt to OpenAI...")
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error querying OpenAI: {e}")
            return ""

    def process_batch(self, batch):
        """
        Process the current batch of rows by constructing a prompt,
        querying OpenAI, and storing the results.
        """
        prompt = "Determine the gender for the following individuals based on their Oscar nominations:\n"
        for j, (year, name, category, film) in enumerate(batch):
            prompt += f"{j + 1}. In {year}, {name} was nominated for Oscar in {category} for the film '{film}'. Please specify their gender as Male or Female.\n"
        prompt += "Response with Male or Female. Start each answer with newline. Answer:"

        # Ask OpenAI
        response = self.ask_openai(prompt)
        self.prompt_to_response_cache.append((prompt, response))

        # Parse response
        response_lines = response.split("\n")
        batch_genders = []
        for res, (_, name, category, film) in zip(response_lines, batch):
            batch_genders.append({
                'name': name,
                'category': category,
                'film': film,
                'gender': res.strip()
            })

        return batch_genders

    def process_data(self):
        """
        Process the entire dataset in batches, querying OpenAI,
        and collecting genders for the entries.
        """
        print("Processing data...")
        temp_batch = []

        for i, row in tqdm.tqdm(self.oscar_award.iterrows(), total=len(self.oscar_award)):
            year = row['year_ceremony']
            name = row['name']
            category = row['category']
            film = row['film']

            # Add the current row to the temporary batch
            temp_batch.append((year, name, category, film))

            # Process the batch when it is full or at the last row
            if len(temp_batch) == self.batch_size or i == len(self.oscar_award) - 1:
                try:
                    genders = self.process_batch(temp_batch)
                    self.genders.extend(genders)
                except Exception as e:
                    print(f"Error processing batch at index {i}: {e}")
                finally:
                    temp_batch = []  # Clear batch after processing

            # Save intermediate results every 1000 entries
            if i % 1000 == 0 and i > 0:
                self.save_results("genders_intermediate.json")

    def save_results(self, output_file: str):
        """ Save the collected gender data to a JSON file. """
        print(f"Saving results to {output_file}...")
        with open(output_file, 'w') as f:
            json.dump(self.genders, f)

    def run(self, output_file: str):
        """ Run the entire process: load data, process it, and save the results. """
        self.load_data()
        self.process_data()
        self.save_results(output_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process Oscar award data using OpenAI.")
    parser.add_argument('--api_key', required=True, help="Your OpenAI API key.")
    parser.add_argument('--input_file', required=True, help="Path to the input Oscar award CSV file.")
    parser.add_argument('--output_file', default='genders_final.json', help="Path to save the output JSON file.")
    parser.add_argument('--batch_size', type=int, default=5, help="Number of records per batch for OpenAI prompts.")

    args = parser.parse_args()

    processor = OscarDataProcessor(
        api_key=args.api_key,
        input_file=args.input_file,
        batch_size=args.batch_size
    )
    processor.run(output_file=args.output_file)