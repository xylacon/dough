import json
import base64
from tqdm import tqdm
from pathlib import Path


def all_batch(img_files:list[Path], prompt:str):
    # initialize tasks
    tasks = []

    # image operations
    for img_path in tqdm(img_files):

        with open(img_path, mode="rb") as img_file:
            # get image id
            img_id = img_path.stem

            # convert image to base64 bytes
            img = base64.b64encode(img_file.read()).decode("utf-8")

        # create task line
        task = {
            "custom_id": f"{img_id}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful document parsing assistant."},
                    {"role": "user", 
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img}",
                                    "detail": "high"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    },
                ],
                "max_tokens": 1000
            }
        }

        tasks.append(task)

    # batch task file path
    batch_path = Path("batch_tasks.jsonl")

    # write to jsonl file
    with open(batch_path, mode="w") as batch_file:
        for task in tasks:
            batch_file.write(json.dumps(task) + "\n")


def divide_list(src:list, n:int) -> list[list]:
    # initialize
    result = []

    # compute chunk size
    size = len(src)
    q, r = divmod(size, n)

    for i in range(0, n):
        if i < r:
            result.append(src[0:(q+1)])
            del src[0:(q+1)]
        else:
            result.append(src[0:q])
            del src[0:q]

    return result


if __name__=="__main__":

    # get the prompt
    with open("gpt_prompt.txt", mode="r") as prompt_file:
        gpt_instructions = "".join([x for x in prompt_file])

    # get a list of all image paths
    files = [x for x in Path("../image_dataset").rglob("*.jpg")]

    # create a single batch file containing all batch tasks
    all_batch(files, gpt_instructions)

    # open the jsonl
    with open("batch_tasks.jsonl", mode="r") as batch_file:
        data = [json.loads(line) for line in batch_file]

    # delete the single batch file
    Path("batch_tasks.jsonl").unlink()

    # divide up the jsonl data into appropriate size chunks (for this dataset, n=100)
    n = 100
    batches = divide_list(data, n)

    # smaller batches directory
    batch_dir = Path("batches/")
    batch_dir.mkdir(exist_ok=True)

    # write to smaller jsonl files in batches directory
    for i in tqdm(range(n)):
        with open(Path(batch_dir / f"batch_{i}.jsonl"), mode="w") as batch_file:
            for task in batches[i]:
                batch_file.write(json.dumps(task) + "\n")
