jq '.reports[] | select(.completeness == "COMPLETE") | .accession' hadv.json
