import functools

R.<x> = QQ[]

quantifier = "e"
formula = {
  "forms": [(x^2 + 2*x + 1, "-"), (x^2 + 2*x + 1, "0")],
  "conn": "or"
}

tests = [
  {
    "quantifier": "e",
    "formula": {
      "forms": [(x^2 + 2*x + 1, "-"), (x^2 + 2*x + 1, "0")],
      "conn": "or"
    }
  },
  {
    "quantifier": "e",
    "formula": {
      "forms": [(x^2 + 2*x + 1, "-"), (x^2 + 2*x + 1, "0")],
      "conn": "and"
    }
  },
  {
    "quantifier": "a",
    "formula": {
      "forms": [
        (x + 2, "0"),
        {
          "form": (x^2 + 1, "0"),
          "conn": "not"
        }
      ],
      "conn": "or"
    }
  },
  {
    "quantifier": "a",
    "formula": {
      "forms": [
        (x^2 + 4*x + 4, "0"),
        {
          "form": (x^3 + 2*x^2 + x + 2, "0"),
          "conn": "not"
        }
      ],
      "conn": "or"
    }
  },
  {
    "quantifier": "e",
    "formula": {
      "forms": [(x^2 + 2*x + 1, "-"), (x^2 + 2*x + 1, "0")],
      "conn": "or"
    }
  },
  {
    "quantifier": "a",
    "formula": {
      "forms": [(x^2, "+"), (x^2, "0")],
      "conn": "or"
    }
  },
  {
    "quantifier": "a",
    "formula": {
      "forms": [(x^3, "+"), (x^3, "0")],
      "conn": "or"
    }
  },
  {
    "quantifier": "a",
    "formula": (x^4 + 1, "+")
  },
]


def signMatrix(pl):
  prod = functools.reduce(lambda a, b: a * b, pl)
  roots = prod.roots(ring=AA, multiplicities=False) # potentially slow
  #print("Roots: {}".format(roots))
  num = 2 * len(roots) + 1
  ret = []
  for i in range(num):
    if i % 2 == 0:
      # interval
      if len(roots) == 0:
        val = 0
      elif i == 0:
        val = roots[0] - 1
      elif i/2 >= len(roots):
        val = roots[len(roots) - 1] + 1
      else:
        val = (roots[i/2 - 1] + roots[i/2]) / 2
    else:
      # root
      val = roots[(i - 1)/2]
    #print("{}: {}".format(i, val))
    d = {}
    for p in pl:
      x = p(val)
      if x > 0:
        d[p] = "+"
      elif x < 0:
        d[p] = "-"
      else:
        d[p] = "0"
    ret.append(d)
  return ret

def plist(f):
  if type(f) == tuple:
    return frozenset([f[0]])
  elif f["conn"] == "not":
    return plist(f["form"])
  else:
    return functools.reduce(lambda a, b: a.union(b), map(lambda x: plist(x), f["forms"]))

def evalForm(f, d):
  if type(f) == tuple:
    return d[f[0]] == f[1]
  else:
    if f["conn"] == "not":
      return not evalForm(f["form"], d)
    if f["conn"] == "or":
      sc = True
    elif f["conn"] == "and":
      sc = False
    for sf in f["forms"]:
      if evalForm(sf, d) == sc:
        # short circuit
        return sc
    return not sc

def strForm(f):
  if type(f) == tuple:
    m = {"+": ">", "-": "<", "0": "="}
    return "({} {} 0)".format(f[0], m[f[1]])
  else:
    if(f["conn"] == "not"):
      return "(not {})".format(strForm(f["form"]))
    l = map(lambda x: strForm(x), f["forms"])
    conn = " " + f["conn"] + " "
    return "({})".format(conn.join(l))

def decide(f, q):
  pl = list(plist(f))
  sm = signMatrix(pl)
  if q == "e":
    sc = True
  elif q == "a":
    sc = False
  for d in sm:
    if evalForm(f, d) == sc:
      return sc
  return not sc

def wrapper(f, q):
  print("Formula: {} {}".format("exists x" if q == "e" else "forall x", strForm(f)))
  print(decide(f, q))
  print()

for (i, t) in enumerate(tests):
  print("Test case {}".format(i))
  wrapper(t["formula"], t["quantifier"])

