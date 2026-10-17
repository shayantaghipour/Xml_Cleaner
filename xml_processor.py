import os
import copy
import xml.etree.ElementTree as ET
from datetime import datetime


def parse_date(text):
    if not text:
        return None

    text = text.strip()

    formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    )

    if text.endswith("Z"):
        text = text[:-1]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass

    return None


def normalize_station(value):
    if value is None:
        return None

    value = value.strip()

    try:
        return str(int(float(value)))
    except Exception:
        return value


def get_adsr_nodes(root):
    adsr = root.findall(".//ADSR")

    if adsr:
        return adsr

    return [x for x in root.iter() if x.tag.endswith("ADSR")]


def process_folder(folder):

    records = {}

    total_files = 0
    total_records = 0
    removed = 0
    skipped = 0

    for file in os.listdir(folder):

        if not file.lower().endswith(".xml"):
            continue

        if file.lower() == "output_clean.xml":
            continue

        path = os.path.join(folder, file)

        try:

            tree = ET.parse(path)
            root = tree.getroot()

            total_files += 1

            for adsr in get_adsr_nodes(root):

                total_records += 1

                station = normalize_station(
                    adsr.findtext("station_no")
                )

                deployment = adsr.findtext("deployment_time")

                if deployment:
                    deployment = deployment.strip()

                if not station or not deployment:
                    skipped += 1
                    continue

                deploy_time = parse_date(deployment)

                if deploy_time is None:
                    skipped += 1
                    continue

                current = records.get(station)

                if current is None:

                    records[station] = {
                        "date": deploy_time,
                        "xml": copy.deepcopy(adsr)
                    }

                else:

                    if deploy_time > current["date"]:

                        records[station] = {
                            "date": deploy_time,
                            "xml": copy.deepcopy(adsr)
                        }

                    removed += 1

        except Exception as ex:

            print(f"[ERROR] {file} -> {ex}")

    output_root = ET.Element("DocumentElement")

    def station_sort(item):
        try:
            return int(item)
        except:
            return item

    for station in sorted(records.keys(), key=station_sort):

        output_root.append(records[station]["xml"])

    output_file = os.path.join(folder, "output_clean.xml")

    ET.ElementTree(output_root).write(
        output_file,
        encoding="utf-8",
        xml_declaration=True
    )

    return (
        f"Files Processed : {total_files}\n"
        f"Records Read : {total_records}\n"
        f"Duplicates Removed : {removed}\n"
        f"Skipped : {skipped}\n"
        f"Remaining Records : {len(records)}\n"
        f"Saved To : {output_file}"
    )