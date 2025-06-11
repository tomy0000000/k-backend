#!/usr/bin/env python
#
# Usage: convert_openapi.py <path_to_openapi.json>
#
# Reference:
# https://fastapi.tiangolo.com/advanced/generate-clients/#preprocess-the-openapi-specification-for-the-client-generator

import json
import sys
from pathlib import Path


def main() -> None:
    # Read input file
    if len(sys.argv) < 2:
        print("Usage: convert_openapi.py <path_to_openapi.json>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
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
