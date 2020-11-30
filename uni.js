// all our polynomials are over the rationals
Polynomial.setField("Q");

function polyEq(p1, p2) {
  return p1.sub(p2).degree() == -Infinity;
}

function mapGet(m, p1) {
  for(e of m) {
    if(polyEq(e["key"], p1)) {
      return e["value"];
    }
  }
  return null;
}

function mapSet(m, p, v) {
  for(e of m) {
    if(polyEq(e["key"], p1)) {
      e["value"] = v;
      return;
    }
  }
  m.push({key: p, value: v})
}

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
var p1 = new Polynomial("1/6x^2+1");
var p2 = new Polynomial("x+2");
var quantifier = "forall"
var formula = {
  conn: "or",
  sf: [
    {
      conn: "not",
      sf: {
        poly: p1,
        signs: ["0"]
      }
    },
    {
      poly: p2,
      signs: ["0"]
    }
  ]
}

console.log(quantifier);
console.log(formula);

// sign matrix is a list of maps mapping polynomials to their signs "+", "-", or "0"

var sm = [
  {map: [{key: p1, value: "+"}, {key: p2, value: "-"}], ty: "neginf"},
  {map: [{key: p1, value: "+"}, {key: p2, value: "0"}], ty: "root"},
  {map: [{key: p1, value: "+"}, {key: p2, value: "+"}], ty: "posinf"},
]

function computeSM(polylist) {
  // find a polynomial of max degree
  var md = -Infinity;
  var mdp;
  for(p of polylist) {
    if(p.degree() > md) {
      md = p.degree();
      mdp = p;
    }
  }

  // base case of recursion
  if(md == 1) {
    // all polynomials are degree 1 (constants). map accordingly
  }

  // build new polylist: p0, p1, ..., pn-1 -> p0', p1, ..., pn-1, p0%p0', p0%p1, ... p0%pn-1
  var p0 = mdp.derive();
  newplist = [p0]
  newqlist = [mdp.div(p0)]
  for(p of polylist) {
    if(p != mdp) {
      newplist.push(p);
      newqlist.push(mdp.mod(p));
    }
  }

  // get sign matrix of new plists
  sm = computeSM(newplist.concat(newqlist));

  // infer signs of mdp at points of type root
  for(e of sm) {
    if(e["ty"] == "root") {
      
    }
  }
}

// compute formula truth from sign matrix

function evalMatrix(mat, sl) {
  if("poly" in mat) {
    // atomic formula, evaluate using sign info
    return mat["signs"].indexOf(mapGet(sl, mat["poly"])) >= 0;
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

function eval(sm) {
  for(e of sm) {
    var sl = e["map"];
    var val = evalMatrix(formula, sl);
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

console.log("RESULT: " + eval(sm));