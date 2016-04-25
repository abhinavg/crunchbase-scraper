def Infos(filename):
  with open(filename) as f:
    return set(pickle.load(f))

def ThisYear(infos):
  return [info for info in infos
          if any(['2014' in fr.date for fr in info.funding_rounds])]

def LastTwoYears(infos):
  return [info for info in infos
          if any(['2014' in fr.date or '2013' in fr.date for fr in info.funding_rounds])]

def NoHq(infos):
  return [info for info in infos if not info.headquarters]

def SF(infos):
  return [info for info in infos if 'San Francisco' in info.headquarters]

def Open(infos):
  return [info for info in infos if not info.status and not info.ipo]

def CuratedWeb(infos):
  return [info for info in infos if 'Curated Web' in info.categories]

def MakeDict(infos):
  return {info.name: info for info in infos}