
import re

class OcrRepair:
    def DoRepair(self):
        raise NotImplementedError()


class ReplaceRepair(OcrRepair):
    def __init__(self, fieldName: str, oldSubstr: str, newSubstr: str):
        self.FieldName = fieldName
        self.OldSubstr = oldSubstr
        self.NewSubstr = newSubstr

    def DoRepair(self, illustrated):
        if not hasattr(illustrated, self.FieldName):
            raise Exception(f'ReplaceRepair field not found. ReplaceRepair:[{self.__dict__}]. illustrated:[{illustrated.__dict__}]')
        setattr(illustrated, self.FieldName, getattr(illustrated, self.FieldName).replace(self.OldSubstr, self.NewSubstr))


class RemixReplaceRepair(OcrRepair):
    def __init__(self, pattern: str, patternField: str, fieldName: str, newStr: str):
        self.Pattern = pattern
        self.PatternField = patternField
        self.FieldName = fieldName
        self.NewStr = newStr

    def DoRepair(self, illustrated):
        if not hasattr(illustrated, self.FieldName) or not hasattr(illustrated, self.PatternField):
            raise Exception(f'ReplaceRepair field not found. ReplaceRepair:[{self.__dict__}]. illustrated:[{illustrated.__dict__}]')
        if re.match(self.Pattern, getattr(illustrated, self.PatternField), flags=0):
            setattr(illustrated, self.FieldName, self.NewStr)
