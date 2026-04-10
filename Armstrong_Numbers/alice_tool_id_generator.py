import pyperclip as pc
from enum import Enum
import os

class AppID(Enum):
    MPA_VOD = "P667348C6-F130-439D-B12F-245F0FB402A0"
    MPA_LS = "P667348C6-F130-439D-B12F-245F0FB402A0"
    MA_ES = "P667348C6-F130-439D-B12F-245F0FB402A0"
    VMS_VOD_VOX = "P1702F598-44CE-42DD-819D-7F636728BD21"

class RRN(Enum):
    STAMM_MPA_VOD = "rrn:watch:videohub:episode:"
    STAMM_MPA_LS = "rrn:watch:videohub:station:"
    STAMM_MA_ES_FOOTBALL = "rrn:watch:live-events:football:"
    STAMM_MA_ES_AMERICAN_FOOTBALL = "rrn:watch:live-events:american-football:"
    STAMM_MA_ES_CONCERT = "rrn:watch:live-events:concert:"
    STAMM_MA_ES_MOTORSPORT = "rrn:watch:live-events:motorsport:"
    STAMM_MA_ES_OTHER = "rrn:watch:live-events:other:"


def build_rrn_string(rrn: RRN, bso_key: str, app_id: AppID) -> str:
    """
    Builds a string in the format: <rrn><bso_key>, <app_id>

    Example:
        rrn:watch:videohub:episode:1023376, P667348C6-F130-439D-B12F-245F0FB402A0

    Args:
        rrn (RRN): The RRN enum value
        bso_key (str): The BSO key
        app_id (AppID): The app ID enum value

    Returns:
        str: The formatted string
    """
    return f"{rrn}{bso_key}, {app_id}"

def build_vms_string(vms_id: str, app_id: AppID) -> str:
    """
    Builds a string in the format: <vms_id>, <app_id>

    Example:
        1023376, P667348C6-F130-439D-B12F-245F0FB402A0, test/ivwtag1

    Args:
        vms_id (str): The VMS ID
        app_id (AppID): The app ID enum value

    Returns:
        str: The formatted string
    """
    return f"{vms_id}, {app_id}, test/ivwtag1"

file_path = os.path.join(os.path.expanduser("~"), "Downloads", "vms_ids.txt")
if not os.path.exists(file_path):
    print(f"Die Datei '{file_path}' existiert nicht. Bitte stelle sicher, dass die Datei im Download-Ordner vorhanden ist.")
    exit(1)

# Datei lesen und BSO Keys extrahieren
with open(file_path, "r") as f:
    # Alle Zeilen lesen, Leerzeilen ignorieren -> line.strip() ist false, wenn die Zeile nur aus Leerzeichen besteht
    bso_keys: list[str] = [stripped_line for line in f if (stripped_line := line.strip())] 

# Alle Strings bauen
#rrn = RRN.STAMM_MPA_VOD.value
app_id = AppID.VMS_VOD_VOX.value
results = [build_vms_string(vms_id, app_id) for vms_id in bso_keys]

# Alles zu einem String zusammenbauen (z. B. mit Zeilenumbrüchen)
output = "\n".join(results)

#Ergebnisse in die Zwischenablage kopieren
pc.copy(output)
