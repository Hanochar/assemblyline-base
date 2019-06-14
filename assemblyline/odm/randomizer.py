import datetime
import random
import rstr
import time

from assemblyline.common.uid import get_random_id
from assemblyline.odm import Boolean, Enum, Keyword, Text, List, Model, Compound, Integer, Float, Date, Mapping, \
    Classification, Optional, Any, forge, ValidatedKeyword, IP, Domain, MD5, SHA1, SHA256, PhoneNumber, MAC, URIPath, \
    URI, SSDeepHash

config = forge.get_config()

ALPHA = "ABCDEFGHIJKLMNOPQRSTUPVXYZabcdefghijklmnopqrstuvwxyz"
HASH_ALPHA = "abcdef0123456789"
SSDEEP_ALPHA = f"{ALPHA}0123456789"
WORDS = """The Cyber Centre stays on the cutting edge of technology by working with commercial vendors of cyber security 
technology to support their development of enhanced cyber defence tools To do this our experts survey the cyber 
security market and evaluate emerging technologies in order to determine their potential to improve cyber security 
across the country The Cyber Centre supports innovation by collaborating with all levels of government private 
industry and academia to examine complex problems in cyber security We are constantly engaging partners to promote 
an open and innovative environment We invite partners to work with us but also promote other Government of Canada 
innovation programs One of our key partnerships is with the Government of Canada Build in Canada Innovation Program 
BCIP The BCIP helps Canadian companies of all sizes transition their state of the art goods and services from the 
laboratory to the marketplace For certain cyber security innovations the Cyber Centre performs the role of technical 
authority We evaluate participating companies new technology and provide feedback in order to assist them in bringing 
their product to market To learn more about selling or testing an innovation visit the BCIP website""".split()
WORDS = list(set(WORDS))
META_KEYS = ["key_a", "key_b", "key_c", "key_d", "key_e", "key_f"]
EXT = [
    ".jpg",
    ".doc",
    ".exe",
    ".pdf",
    ".xls",
    ".lnk",
    ".gif",
    ".ppt"
]

DOM = [
    ".com",
    ".ca",
    ".biz",
    ".edu"
]

SERVICES = {
    "Beaver": ("External", "FILTER"),
    "NSRL": ("Filtering", "FILTER"),
    "PEFile": ("Static Analysis", "CORE"),
    "Extract": ("Extraction", "EXTRACT"),
    "TagCheck": ("Static Analysis", "POST"),
    "PDFId": ("Static Analysis", "CORE"),
    "PeePDF": ("Static Analysis", "CORE"),
    "Characterize": ("Static Analysis", "CORE"),
    "FrankenStrings": ("Static Analysis", "SECONDARY"),
    "APKaye": ("Static Analysis", "CORE"),
    "Cuckoo": ("Dynamic Analysis", "CORE"),
    "McAfee": ("Antivirus", "CORE"),
    "Metadefender": ("Antivirus", "CORE"),
    "Suricata": ("Networking", "SECONDARY")
}

LABELS = [
    "CAMPAIGN_1",
    "CAMPAIGN_2",
    "CAMPAIGN_3",
    "CAMPAIGN_4",
    "CAMPAIGN_5",
    "PHISHING",
    "SMTP",
    "HTTP",
    "COMPROMISED"
]

USERS = [
    "admin",
    "user"
]

GROUPS = ["USERS", "ADMINS", "ANALYSTS"]

F_TYPES = [
    "image/png",
    "executable/windows",
    "document/pdf",
    "document/office",
    "document/xml",
    "code/javascript",
    "code/vb"
]


def get_random_file_type():
    return random.choice(F_TYPES)


def get_random_word():
    return random.choice(WORDS)


def get_random_phrase(wmin=2, wmax=6):
    return " ".join([get_random_word() for _ in range(random.randint(wmin, wmax))])


def get_random_hash(hash_len):
    return "".join([random.choice(HASH_ALPHA) for _ in range(hash_len)])


def get_random_heuristic_id():
    return f"AL_{get_random_service_name().upper()}_{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}"


def get_random_label():
    return random.choice(LABELS)


def get_random_user():
    return random.choice(USERS)


def get_random_groups():
    return random.choice(GROUPS)


def get_random_filename(smin=1, smax=3):
    return "_".join([get_random_word().lower() for _ in range(random.randint(smin, smax))]) + random.choice(EXT)


def get_random_directory(smin=2, smax=6):
    return "/".join([get_random_word().lower() for _ in range(random.randint(smin, smax))])


def get_random_string(smin=4, smax=24):
    return "".join([random.choice(ALPHA) for _ in range(random.randint(smin, smax))])


def get_random_host():
    return get_random_word().lower() + random.choice(DOM)


def get_random_service_name():
    return random.choice(list(SERVICES.keys()))


def get_random_service_version():
    return f"4.0.0.{get_random_hash(7)}"


def get_random_ip():
    return ".".join([str(random.randint(1, 254)) for _ in range(4)])


def get_random_iso_date(epoch=None):
    if epoch is None:
        epoch = time.time() + random.randint(-10000, 10000)

    return datetime.datetime.fromtimestamp(epoch).isoformat() + "Z"


def get_random_mapping(field):
    return {META_KEYS[i]: random_data_for_field(field, META_KEYS[i]) for i in range(random.randint(0, 5))}


def get_random_phone():
    return f'{random.choice(["", "+1 "])}{"-".join([str(random.randint(100, 999)) for _ in range(3)])}' \
        f'{str(random.randint(0, 9))}'


def get_random_mac():
    return ":".join([get_random_hash(2) for _ in range(6)])


def get_random_uri_path():
    return f"/{'/'.join([get_random_word() for _ in range(random.randint(2, 6))])}"


def get_random_uri():
    return f"{random.choice(['http', 'https', 'ftp'])}://{get_random_host()}{get_random_uri_path()}"


def get_random_ssdeep():
    return f"{str(random.randint(30, 99999))}" \
        f":{''.join([random.choice(SSDEEP_ALPHA) for _ in range(random.randint(20, 64))])}" \
        f":{''.join([random.choice(SSDEEP_ALPHA) for _ in range(random.randint(20, 64))])}"


# noinspection PyProtectedMember
def random_data_for_field(field, name, minimal=False):
    if isinstance(field, Boolean):
        return random.choice([True, False])
    elif isinstance(field, Classification):
        if field.engine.enforce:
            possible_classifications = list(field.engine._classification_cache)
            possible_classifications.extend([field.engine.UNRESTRICTED, field.engine.RESTRICTED])
        else:
            possible_classifications = [field.engine.UNRESTRICTED]
        return random.choice(possible_classifications)
    elif isinstance(field, Enum):
        return random.choice([x for x in field.values if x is not None])
    elif isinstance(field, List):
        return [random_data_for_field(field.child_type, name) if not isinstance(field.child_type, Model)
                else random_model_obj(field.child_type, as_json=True) for _ in range(random.randint(1, 4))]
    elif isinstance(field, Compound):
        if minimal:
            return random_minimal_obj(field.child_type, as_json=True)
        else:
            return random_model_obj(field.child_type, as_json=True)
    elif isinstance(field, Mapping):
        return get_random_mapping(field.child_type)
    elif isinstance(field, Optional):
        if not minimal:
            return random_data_for_field(field.child_type, name)
        else:
            return field.child_type.default
    elif isinstance(field, Date):
        return get_random_iso_date()
    elif isinstance(field, Integer):
        return random.randint(128, 4096)
    elif isinstance(field, Float):
        return random.randint(12800, 409600) / 100.0
    elif isinstance(field, MD5):
        return get_random_hash(32)
    elif isinstance(field, SHA1):
        return get_random_hash(40)
    elif isinstance(field, SHA256):
        return get_random_hash(64)
    elif isinstance(field, SSDeepHash):
        return get_random_ssdeep()
    elif isinstance(field, URI):
        return get_random_uri()
    elif isinstance(field, URIPath):
        return get_random_uri_path()
    elif isinstance(field, MAC):
        return get_random_mac()
    elif isinstance(field, PhoneNumber):
        return get_random_phone()
    elif isinstance(field, IP):
        return get_random_ip()
    elif isinstance(field, Domain):
        return get_random_host()
    elif isinstance(field, ValidatedKeyword):
        return rstr.xeger(field.validation_regex.pattern)
    elif isinstance(field, Keyword):
        if name:
            if "sha256" in name:
                return get_random_hash(64)
            elif "filetype" in name:
                return get_random_file_type()
            elif "organisation" in name:
                return config.system.organisation
            elif "poc" in name:
                return f"{get_random_user()}@{config.system.organisation.lower()}"
            elif "yara_version" in name:
                return random.choice(['3.1', '3.2', '3.3', '3.4'])
            elif "heur_id" in name:
                return get_random_heuristic_id()
            elif "label" in name:
                return get_random_label()
            elif "groups" in name:
                return get_random_groups()
            elif "owner" in name or "uname" in name or "submitter" in name or "created_by" in name:
                return get_random_user()
            elif "service_name" in name:
                return get_random_service_name()
            elif "service_version" in name:
                return get_random_service_version()
            elif "sid" in name or "ingest_id" in name or "workflow_id" in name:
                return get_random_id()
            elif "mac" in name:
                return get_random_hash(12).upper()
            elif "sha1" in name:
                return get_random_hash(40)
            elif "md5" in name or "scan_key" in name or "alert_id" in name:
                return get_random_hash(32)
            elif "host" in name or "node" in name or "domain" in name:
                return get_random_host()
            elif name.endswith("ip") or name.startswith("ip_"):
                return get_random_ip()
            elif "file" in name:
                return get_random_filename()
            elif "name" in name:
                return get_random_filename()
            elif "directory" in name:
                return get_random_directory()

        return get_random_word()
    elif isinstance(field, Text):
        return get_random_phrase(wmin=4, wmax=40)
    elif isinstance(field, Any):
        return get_random_word()
    else:
        raise ValueError(f"Unknown field type {field.__class__}")


# noinspection PyProtectedMember
def random_model_obj(model, as_json=False):
    data = {}
    for f_name, f_value in model._odm_field_cache.items():
        data[f_name] = random_data_for_field(f_value, f_name)

    if as_json:
        return data
    else:
        return model(data)


# noinspection PyProtectedMember
def random_minimal_obj(model, as_json=False):
    data = {}
    for f_name, f_value in model._odm_field_cache.items():
        if not f_value.default_set:
            data[f_name] = random_data_for_field(f_value, f_name, minimal=True)

    if as_json:
        return data
    else:
        return model(data)
