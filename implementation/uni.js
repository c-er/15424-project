// define formula to decide up here
// atomic formulae are defined as {poly: polynomial, signs: [list of signs]}
// where the polynomial representation is described below
// e.g. x^3 + 2x + 3 > 0 becomes {poly: [3, 2, 0, 1], signs: ["+"]}
//     x^3 + 2x + 3 >= 0 becomes {poly: [3, 2, 0, 1], signs: ["+", "0"]}
//      x^3 + 2x + 3 = 0 becomes {poly: [3, 2, 0, 1], signs: ["0"]}
// connectives are defined as {sf: subformula(s), conn: or | and | not}
// in the case of or/and connective, sf is expected to be a list of subformulae
// for not, it is a single subformula

// quantifier on the (single, for now) variable is defined separately below
var p1 = new Polynomial("0.2x^2-0.2");
var p2 = new Polynomial("0.05x^3+0.15x^2+0.15x+0.05");
var p3 = new Polynomial("-0.25x+0.25");
var quantifier = "forall"
var formula = {
  conn: "or",
  sf: [
    {
      conn: "and",
      sf: [
        {
          poly: p1,
          signs: ["+", "0"]
        },
        {
          poly: p2,
          signs: ["+", "0"]
        }
      ]
    },
    {
      poly: p3,
      signs: ["+"]
    }
  ]
}

var x = {
  quantifier: "forall",
  formula: {
    conn: "or",
    sf: [
      {
        conn: "and",
        sf: [
          {
            poly: new Polynomial("4x^2-4"),
            signs: ["+", "0"]
          },
          {
            poly: new Polynomial("x^3+3x^2+3x+1"),
            signs: ["+", "0"]
          }
        ]
      },
      {
        poly: new Polynomial("-5x+5"),
        signs: ["+"]
      }
    ]
  }
}

function flipSign(x) {
  if(x == "+") {
    return "-";
  } else if(x == "-") {
    return "+"
  } else if(x == "0") {
    return "0"
  } else {
    throw "illegal sign";
  }
}

// sign matrix is a list of maps mapping polynomials to their signs "+", "-", or "0"


function assert(b) {
  if(b == true) {
    return;
  }
  throw "assertion failure";
}

function atomToString(a) {
  return "sign(" + a.poly.toString() + ") in " + a.signs;
}

// compute formula truth from sign matrix

function evalMatrix(mat, sl) {
  if("poly" in mat) {
    // atomic formula, evaluate using sign info
    var ret = mat["signs"].indexOf(mapGet(sl, mat["poly"])) >= 0;
    log("Atom {" + atomToString(mat) + "} is " + ret, "outputUni");
    return ret;
  }
  if(mat["conn"] == "not") {
    return !evalMatrix(mat["sf"], sl);
  }
  for(subform of mat["sf"]) {
    var val = evalMatrix(subform, sl)
    if(mat["conn"] == "and" && !val) {
      return false;
    } else if(mat["conn"] == "or" && val) {
      return true;
    }
  }
  if(mat["conn"] == "and") {
    return true;
  } else if (mat["conn"] == "or") {
    return false;
  } else {
    console.log("illegal connective probably");
  }
}

function evalForm(quantifier, formula, sm) {
  for(e of sm) {
    log("SM Row: ", "outputUni");
    printSMrow(e, false, "outputUni");
    var sl = e.map;
    var val = evalMatrix(formula, sl);
    log("Formula is " + val + " on this row", "outputUni");
    log("", "outputUni");
    if(quantifier == "forall" && !val) {
      return false;
    } else if(quantifier == "exists" && val) {
      return true;
    }
  }
  if(quantifier == "forall") {
    return true;
  } else if(quantifier == "exists") {
    return false;
  } else {
    console.log("illegal quantifier probably");
  }
}

function getPlist(form) {
  if("poly" in form) {
    // atomic formula: return singleton
    return [form["poly"]]
  }
  if(form["conn"] == "not") {
    return getPlist(form["sf"]);
  } else if(form["conn"] == "and" || form["conn"] == "or") {
    var m = []
    for(subform of form["sf"]) {
      var res = getPlist(subform);
      for(p of res) {
        mapSet(m, p, "");
      }
    }
    return m.map(x => x.key);
  } else {
    console.log("illegal connective probably");
  }
}

function doUniFull() {
  document.getElementById("outputUni").innerHTML = "";
  eval("var raw_inp = " + document.getElementById("form-inp").value);
  q = raw_inp["quantifier"];
  form = raw_inp["formula"];
  pl = getPlist(form);
  log("Polynomials: " + pl.map(x => x.toString()), "outputUni");
  sm = computeSM(pl, true);
  log("Sign Matrix:", "outputUni");
  printSM(sm, false, "outputUni");
  log("Evaluating:", "outputUni");
  res = evalForm(q, form, sm);
  log("FINAL RESULT: " + res, "outputUni");
}

// console.log("RESULT: " + eval(sm));