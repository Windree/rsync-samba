from path import Path


class Paths:
    def __init__(self, source: str, destination: str):
        source = Path(source)
        destination = Path(destination)

    def validate(self):
        if len(self.source.warnings):
            showWarnings("Source", self.source.warnings)
        if len(self.destination.warnings):
            showWarnings("Destination", self.destination.warnings)
        return not (len(self.source.warnings) or len(self.destination.warnings))


def showWarnings(header: str, warnings: list[str]):
    print("%s:" % (header))
    for warning in warnings:
        print("\t%s" % (warning))
