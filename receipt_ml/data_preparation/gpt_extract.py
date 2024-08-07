import json
from tqdm import tqdm
from pathlib import Path


def main(files_path:list[Path]) -> dict:
    # initialize the dictionaries
    result = {}
    errors = []

    for file in tqdm(files_path):

        # open the file
        with open(file, mode="r") as batch_file:

            for line in batch_file:
                # load the line as a dict
                gpt_response = json.loads(line)

                # grab the file name (id)
                key_val = gpt_response["custom_id"]

                # grab gpt's json reponse
                response = gpt_response["response"]["body"]["choices"][0]["message"]["content"][7:-3]

                # try converting the response to a dict
                try:
                    ground_truth = json.loads(response)

                    # update the result dict
                    result.update({key_val: ground_truth})

                except json.decoder.JSONDecodeError as err_name:
                    errors.append({"file": str(file), "key_value": key_val, "response": response, "error": str(err_name)})

    # write errors to a file      
    with open("gpt_errors.json", mode="w") as error_file:
        json.dump(errors, error_file, indent=4)
    
    return result


if __name__ == "__main__":
    # path to gpt responses
    batch_path = [x for x in Path("gpt_results").rglob("*.jsonl")]

    # dictionary of all ground truth dictionaries
    data = main(batch_path)
