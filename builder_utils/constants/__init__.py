from enum import Enum

class FileName (Enum):
    CONFIG = "config.json"

class FileType (Enum):
    PROBLEM = "problem"
    META = "meta"
    OTHER = "other"

RequiredJsonKeysCommon = {
    "fileType" : str,
    "templateFileName": str,
    "title": str,
}

RequiredJsonKeysProblem = {
    "problemTitle": str,
    "problemId": str,
    "problemStatement": str,
    "inputDescription": str,
    "inputFilePath": str,
    "outputDescription": str,
    "outputFilePath": str,
    "moreInformation": str,
    "judgeFilePath": str,
    "examples": list,
}

RequiredJsonKeysMeta = {
}
