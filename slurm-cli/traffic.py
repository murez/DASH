import jobs


def GetFreeCard() -> str:
    cards = jobs.GetAllCards() # (ID, CARDNAME, InUSE, LIMIT_)
    if cards == [-1]:
        print("GetAllCards failed")
        return None
    for i in cards:
        if i[3] > i[2]:
            return i[1]
    return None

def GetFreeCardFromPCluster() -> str:
    cards = jobs.GetAllCardsFromPCluster() # (ID, CARDNAME, InUSE, LIMIT_)
    if cards == [-1]:
        print("GetAllCardsFromPCluster failed")
        return None
    for i in cards:
        if i[3] > i[2]:
            return i[1]
    return None