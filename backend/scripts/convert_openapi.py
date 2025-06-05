#!/usr/bin/env python
# Reference:
# https://fastapi.tiangolo.com/advanced/generate-clients/#preprocess-the-openapi-specification-for-the-client-generator
import json
from pathlib import Path


def main() -> None:
    file_path = Path("./openapi.json")
    openapi_content = json.loads(file_path.read_text())

    for path_data in openapi_content["paths"].values():
        for operation in path_data.values():
            tag = operation["tags"][0]
            operation_id = operation["operationId"]
            to_remove = f"{tag}-"
            new_operation_id = operation_id[len(to_remove) :]
            operation["operationId"] = new_operation_id

    file_path.write_text(json.dumps(openapi_content))


if __name__ == "__main__":
    main()
