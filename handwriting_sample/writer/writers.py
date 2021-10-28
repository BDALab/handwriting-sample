import json
from handwriting_sample.base import LoggableObject


# ------------ #
# File writers #
# ------------ #

class JSONFileWriter(LoggableObject):
    """Class implementing JSON file writer"""

    @classmethod
    def write(cls, path, data, meta=None, verbose=False):
        """Writes the handwriting data and meta data to a JSON file"""
        try:
            with open(path, "w") as f:
                json.dump({"meta_data": meta, "data": data}, f)
                cls.log(f"Data stored in a JSON file: {path}", be_verbose=verbose)
                return True
        except Exception as e:
            cls.log(f"Unable to store to a JSON file: {path} due to {e}")
            raise


class SVCFileWriter(LoggableObject):
    """Class implementing SVC file writer"""

    @classmethod
    def write(cls, path, data, meta=None, verbose=False):
        """Writes the handwriting data and meta data to an SVC file"""
        try:
            with open(path, "w") as f:
                f.writelines(f"{meta.get('samples_count')}\n")
                f.writelines(data)
                cls.log(f"Data stored in an SVC file: {path}", be_verbose=verbose)
        except Exception as e:
            cls.log(f"Unable to store to an SVC file: {path} due to {e}")
            raise
