// all our polynomials are over the rationals
Polynomial.setField("Q");

function polyEq(p1, p2) {
  return p1.sub(p2).degree() == -Infinity;
}

function mapGet(m, p) {
  for(e of m) {
    if(polyEq(e["key"], p)) {
      return e["value"];
    }
  }
  return null;
}

function mapSet(m, p, v) {
  for(e of m) {
    if(polyEq(e["key"], p)) {
      e["value"] = v;
      return;
    }
  }
  m.push({key: p, value: v})
}

function mapCopy(m) {
  var m2 = [];
  for(e of m) {
    m2.push({key: e.key, value: e.value});
  }
  return m2;
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
// var p1 = new Polynomial("0.2x^2-0.2");
// var p2 = new Polynomial("0.05x^3+0.15x^2+0.15x+0.05");
// var p3 = new Polynomial("-0.25x+0.25");
// var quantifier = "forall"
// var formula = {
//   conn: "or",
//   sf: [
//     {
//       conn: "and",
//       sf: [
//         {
//           poly: p1,
//           signs: ["+", "0"]
//         },
//         {
//           poly: p2,
//           signs: ["+", "0"]
//         }
//       ]
//     },
//     {
//       poly: p3,
//       signs: ["+"]
//     }
//   ]
// }

var p1 = new Polynomial("x^2+0.000001");
var quantifier = "forall"
var formula = {
  poly: p1,
  signs: ["+"]
}

// console.log(quantifier);
// console.log(formula);

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

function printSM(sm) {
  for(row of sm) {
    s = row.ty + ": ";
    for(e of row.map) {
      s += "(" + e.key.toString() + ", " + e.value + "), "
    }
    console.log(s);
  }
}

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

  console.log("MAX: ", mdp.toString());

  // base case of recursion
  if(md <= 0) {
    // all polynomials are constants. map accordingly
    var m = [];
    for(p of polylist) {
      var cmp;
      try {
        cmp = p.lc().compare(new Fraction('0'))
      } catch(err) {
        cmp = 0;
      }
      if(cmp > 0) {
        mapSet(m, p, "+");
      } else if(cmp < 0) {
        mapSet(m, p, "-");
      } else if(cmp == 0) {
        mapSet(m, p, "0");
      } else {
        console.log("JS WTF");
      }
    }
    return [{map: m, ty: "inf"}]
  }

  // build new polylist: p, p1, ..., pn -> p0, p1, ..., pn, p%p0, p%p1, ... p%pn
  // p0 = p'
  var p0 = mdp.derive();
  var newplist = [p0]
  var pmodp0 = mdp.mod(p0);
  var newqlist;
  if(pmodp0.degree() < 0) {
    newqlist = []
  } else {
    newqlist = [mdp.mod(p0)]
  }
  var hasZero = false;
  for(p of polylist) {
    if(p != mdp && p.degree() >= 0) {
      newplist.push(p);
      if(p.degree() >= 0) {
        newqlist.push(mdp.mod(p));
      } else {
        newqlist.push(null);
      }
    }
    if(p.degree() < 0 || mdp.mod(p).degree() < 0) {
      hasZero = true;
    }
  }

  // console.log("NEW PS: ", newplist.map(x => x.toString()));
  // console.log("NEW QS: ", newqlist.map(x => ));

  // get sign matrix of new plists
  // de-dup new plist
  var m = [];
  var tmp = newplist.concat(newqlist);
  for(p of tmp) {
    if(p) {
      mapSet(m, p, "");
    }
  }
  var reclist = m.map(x => x.key);
  console.log("REC POLYS: ", reclist.map(x => x.toString()));
  var sm = computeSM(reclist);

  // add zero back in if necessary
  if(hasZero) {
    var newsm = [];
    for(row of sm) {
      var m = mapCopy(row.map); mapSet(m, new Polynomial("0"), "0");
      newsm.push({map: m, ty: row.ty})
    }
    sm = newsm;
  }
  
  console.log("Got rec SM: ");
  printSM(sm);

  console.log("NEWPLIST: ", newplist.map(x => x.toString()));

  function isRootP(row) {
    if(row.ty != "root") {
      return null;
    }
    for(var i = 0; i < newplist.length; i++) {
      if(mapGet(row.map, newplist[i]) == "0") {
        assert(newplist[i].degree() >= 0);
        return mdp.mod(newplist[i]);
      }
    }
    return null;
  }

  // figure out signs of removed polynomial at roots
  for(var i = 0; i < sm.length ; i++) {
    // if this row is the root of some "p-list" polynomial
    var q = isRootP(sm[i]);
    if(q) {
      // copy sign from corresponding remainder to mdp
      console.log("remainder: " + q.toString());
      mapSet(sm[i].map, mdp, mapGet(sm[i].map, q));
    }
  }

  console.log("Pre-death 1");
  printSM(sm);

  // delete unnecessary information from sm
  var newsm = [];
  for(var i = 0; i < sm.length ; i++) {
    // if this row is the root of some "p-list" polynomial, OR its not a root at all
    var q = isRootP(sm[i]);
    if(q || sm[i].ty != "root") {
      var m = [];
      // retain only the necessary entries
      for(p of (newplist.concat([mdp]))) {
        mapSet(m, p, mapGet(sm[i].map, p));
      }
      newsm.push({map: m, ty: sm[i].ty});
    } else {
      // then we can discard it - we don't need it anymore and it doesn't belong in the output
    }
  }
  sm = newsm;

  console.log("Pre-death 2");
  printSM(sm);

  // go through newsm and inject roots as necessary/infer signs in intervals
  var newsm = [];
  for(var i = 0; i < sm.length; i++) {
    console.log("Processing: ", sm[i].ty);
    if(sm[i].ty == "inf") {
      assert(sm.length == 1); // should be only entry
      var leftSign = flipSign(mapGet(sm[i].map, p0));
      var rightSign = mapGet(sm[i].map, p0);
      console.log("Left sign: ", leftSign, " and right sign: ", rightSign);
      if((leftSign == "-" && rightSign == "+") || (leftSign == "+" && rightSign == "-")) {
        // inject root
        console.log("root in interval!!");
        var ml = mapCopy(sm[i].map); mapSet(ml, mdp, leftSign);
        var mr = mapCopy(sm[i].map); mapSet(mr, mdp, rightSign);
        var m0 = mapCopy(sm[i].map); mapSet(m0, mdp, "0");
        console.log(newsm);
        newsm = newsm.concat([
          {map: ml, ty: "neginf"},
          {map: m0, ty: "root"},
          {map: mr, ty: "posinf"}
        ]);
        console.log(newsm);
      } else {
        // no root in interval - copy value from either endpoint
        // impossible for this case
        throw "wtf happened here";
      }
    } else if(sm[i].ty == "neginf") {
      assert(i == 0); // should only happen as first entry
      var leftSign = flipSign(mapGet(sm[i].map, p0));
      assert(sm[i + 1].ty == "root"); // next entry should be a root
      var rightSign = mapGet(sm[i + 1].map, mdp); // get sign of poly at leftmost root
      // check for sign change - indicates root in interval
      if((leftSign == "-" && rightSign == "+") || (leftSign == "+" && rightSign == "-")) {
        // inject root
        var ml = mapCopy(sm[i].map); mapSet(ml, mdp, leftSign);
        var mr = mapCopy(sm[i].map); mapSet(mr, mdp, rightSign);
        var m0 = mapCopy(sm[i].map); mapSet(m0, mdp, "0");
        newsm = newsm.concat([
          {map: ml, ty: "neginf"},
          {map: m0, ty: "root"},
          {map: mr, ty: "interval"}
        ]);
      } else {
        // no root in interval - copy value from either endpoint
        var m = mapCopy(sm[i].map); mapSet(m, mdp, rightSign);
        newsm.push({map: m, ty: "neginf"});
      }
    } else if(sm[i].ty == "posinf") {
      assert(i == sm.length - 1); // should only happen as last entry
      var rightSign = mapGet(sm[i].map, p0); // derivative tells us what happens as we go to inf
      assert(sm[i - 1].ty == "root"); // previous entry should be a root
      var leftSign = mapGet(sm[i - 1].map, mdp);
      // check for sign change - indicates root in interval
      if((leftSign == "-" && rightSign == "+") || (leftSign == "+" && rightSign == "-")) {
        // inject root
        var ml = mapCopy(sm[i].map); mapSet(ml, mdp, leftSign);
        var mr = mapCopy(sm[i].map); mapSet(mr, mdp, rightSign);
        var m0 = mapCopy(sm[i].map); mapSet(m0, mdp, "0");
        newsm = newsm.concat([
          {map: ml, ty: "interval"},
          {map: m0, ty: "root"},
          {map: mr, ty: "posinf"},
        ]);
      } else {
        // no root in interval - copy value from either endpoint
        var m = mapCopy(sm[i].map); mapSet(m, mdp, leftSign);
        newsm.push({map: m, ty: "posinf"});
      }
    } else if(sm[i].ty == "interval") {
      assert(sm[i - 1].ty == "root" && sm[i + 1].ty == "root"); // surrounded by roots
      var leftSign = mapGet(sm[i - 1].map, mdp);
      var rightSign = mapGet(sm[i + 1].map, mdp);
      // check for sign change - indicates root in interval
      if((leftSign == "-" && rightSign == "+") || (leftSign == "+" && rightSign == "-")) {
        // inject root
        var ml = mapCopy(sm[i].map); mapSet(ml, mdp, leftSign);
        var mr = mapCopy(sm[i].map); mapSet(mr, mdp, rightSign);
        var m0 = mapCopy(sm[i].map); mapSet(m0, mdp, "0");
        newsm = newsm.concat([
          {map: ml, ty: "interval"},
          {map: m0, ty: "root"},
          {map: mr, ty: "interval"},
        ]);
      } else {
        // no root in interval - copy value from either endpoint
        var m = mapCopy(sm[i].map); mapSet(m, mdp, leftSign);
        newsm.push({map: m, ty: "interval"});
      }
    } else if(sm[i].ty == "root") {
      // root signs should already be calculated
      var s = mapGet(sm[i].map, mdp);
      assert(s != null);
      var m = mapCopy(sm[i].map)
      newsm.push({map: m, ty: "root"});
    } else {
      throw "illegal row type";
    }
  }

  console.log("Pre-death 3");
  printSM(newsm);
  console.log("POLYS: ", polylist.map(x => x.toString()));

  // final filter
  var retsm = [];
  for(row of newsm) {
    var m = [];
    for(p of polylist) {
      if(mapGet(row.map, p) == null) {
        assert(p.degree() < 0);
        mapSet(m, p, "0");
        continue;
      }
      mapSet(m, p, mapGet(row.map, p));
    }
    retsm.push({map: m, ty: row.ty});
  }

  console.log("RETURNING");
  printSM(retsm);
  console.log("we out this bitch");
  
  return retsm;
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

function eval(quantifier, formula, sm) {
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

var plist = getPlist(formula);
console.log("Polynomial list: ", plist.map(x => x.toString()));
var sm = computeSM(plist);
console.log("Sign matrix: ");
printSM(sm);
var res = eval(quantifier, formula, sm);
console.log("Result: ", res);

// console.log("RESULT: " + eval(sm));