from logger import Info, Error, Debug

if __name__ == "__main__":

    logger = Info(Debug(Error()))

    logger.log("ERROR", "Image not synced")
    logger.log("DEBUG", "Distance came out as 0")
    logger.log("INFO", "Rider is unavailable")