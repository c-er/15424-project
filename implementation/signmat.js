// all our polynomials are over the rationals
Polynomial.setField("Q");

// polynomial equality, because its not provided by the library
function polyEq(p1, p2) {
  return p1.sub(p2).degree() == -Infinity;
}

// maps on polynomials, via key-value pair lists
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

var printRec;

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

// output

function log(s) {
  var loc = document.getElementById("output");
  var text = document.createTextNode(s + "\n");
  loc.appendChild(text);
}

function log_sil(s, sil) {
  if(sil) {
    return;
  }
  var loc = document.getElementById("output");
  var text = document.createTextNode(s + "\n");
  loc.appendChild(text);
}

// print a sign matrix

function printSM(sm, sil) {
  for(row of sm) {
    s = row.ty + ": ";
    for(e of row.map) {
      s += "(" + e.key.toString() + ", " + e.value + "), "
    }
    log_sil(s, sil);
  }
  log_sil("", sil);
}

function printSMrow(row, sil) {
  s = row.ty + ": ";
  for(e of row.map) {
    s += "(" + e.key.toString() + ", " + e.value + "), "
  }
  log_sil(s, sil);
}

function computeSM(polylist, silent) {
  log_sil("Input polynomials: " + polylist.map(x => x.toString()), silent);
  // find a polynomial of max degree
  var md = -Infinity;
  var mdp = null;
  for(p of polylist) {
    if(p.degree() > md) {
      md = p.degree();
      mdp = p;
    }
  }

  function nulltoString(x) {
    if(x == null) {
      return "null";
    }
    return x.toString();
  }

  log_sil("p_1 (of max degree): " + nulltoString(mdp), silent);

  // base case of recursion
  if(md <= 0) {
    log_sil("Base case", silent);
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
  var newqlist = [pmodp0];
  var hasZero = false;
  if(pmodp0.degree() < 0) {
    hasZero = true;
  }
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

  log_sil("p_1', p_2, ..., p_n: " + newplist.map(x => x.toString()), silent);
  log_sil("Remainders: " + newqlist.map(nulltoString), silent);

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
  log_sil("Recursive call on: " + reclist.map(x => x.toString()), silent);
  var sm;
  if(printRec) {
    sm = computeSM(reclist, silent);
  } else {
    sm = computeSM(reclist, true);
  }

  // add zero back in if necessary
  if(hasZero) {
    var newsm = [];
    for(row of sm) {
      var m = mapCopy(row.map); mapSet(m, new Polynomial("0"), "0");
      newsm.push({map: m, ty: row.ty})
    }
    sm = newsm;
  }
  
  log_sil("Recursive result: ", silent);
  printSM(sm, silent);

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

  log_sil("Determining sign of p_1 at roots of p_1', p_2, ..., p_n:", silent);

  // figure out signs of removed polynomial at roots
  for(var i = 0; i < sm.length ; i++) {
    // if this row is the root of some "p-list" polynomial
    var q = isRootP(sm[i]);
    if(q) {
      // copy sign from corresponding remainder to mdp
      mapSet(sm[i].map, mdp, mapGet(sm[i].map, q));
    }
  }

  printSM(sm, silent);

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
  newsm = [];
  var i = 0;
  while(i < sm.length) {
    l = [];
    while(i < sm.length && (sm[i].ty == "interval" || sm[i].ty == "neginf" || sm[i].ty == "posinf")) {
      l.push({map: mapCopy(sm[i].map), ty: sm[i].ty});
      i++;
    }
    if(l.length == 0) {
      newsm.push({map: mapCopy(sm[i].map), ty: sm[i].ty});
      i++;
      continue;
    } else if(l[0].ty == "neginf" && l[l.length - 1].ty == "posinf") {
      newsm.push({map: l[0].map, ty: "inf"});
    } else if(l[0].ty == "neginf") {
      newsm.push({map: l[0].map, ty: "neginf"});
    } else if(l[l.length - 1].ty == "posinf") {
      newsm.push({map: l[l.length - 1].map, ty: "posinf"});
    } else {
      newsm.push({map: l[0].map, ty: "interval"});
    }
  }

  sm = newsm;

  log_sil("Removing remainder information: ", silent);
  printSM(sm, silent);

  log_sil("Determining sign on intervals: ", silent);

  // go through newsm and inject roots as necessary/infer signs in intervals
  var newsm = [];
  for(var i = 0; i < sm.length; i++) {
    log_sil("Processing row of type: " + sm[i].ty, silent);
    if(sm[i].ty == "inf") {
      assert(sm.length == 1); // should be only entry
      var leftSign = flipSign(mapGet(sm[i].map, p0));
      var rightSign = mapGet(sm[i].map, p0);
      log_sil("Context:", silent);
      printSMrow(sm[i], silent);
      log_sil("Left sign: " + leftSign + " right sign: " + rightSign, silent);
      if((leftSign == "-" && rightSign == "+") || (leftSign == "+" && rightSign == "-")) {
        // inject root
        log_sil("Injecting root in interval", silent);
        var ml = mapCopy(sm[i].map); mapSet(ml, mdp, leftSign);
        var mr = mapCopy(sm[i].map); mapSet(mr, mdp, rightSign);
        var m0 = mapCopy(sm[i].map); mapSet(m0, mdp, "0");
        newsm = newsm.concat([
          {map: ml, ty: "neginf"},
          {map: m0, ty: "root"},
          {map: mr, ty: "posinf"}
        ]);
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
      assert(leftSign != null && rightSign != null);
      log_sil("Context:", silent);
      printSMrow(sm[i], silent);
      printSMrow(sm[i + 1], silent);
      // check for sign change - indicates root in interval
      log_sil("Left sign: " + leftSign + " right sign: " + rightSign, silent);
      if((leftSign == "-" && rightSign == "+") || (leftSign == "+" && rightSign == "-")) {
        // inject root
        log_sil("Injecting root in interval", silent);
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
        log_sil("No root in interval: taking sign as we go to -inf", silent);
        var m = mapCopy(sm[i].map); mapSet(m, mdp, leftSign);
        newsm.push({map: m, ty: "neginf"});
      }
    } else if(sm[i].ty == "posinf") {
      assert(i == sm.length - 1); // should only happen as last entry
      var rightSign = mapGet(sm[i].map, p0); // derivative tells us what happens as we go to inf
      assert(sm[i - 1].ty == "root"); // previous entry should be a root
      var leftSign = mapGet(sm[i - 1].map, mdp);
      assert(leftSign != null && rightSign != null);
      log_sil("Context:", silent);
      printSMrow(sm[i - 1], silent);
      printSMrow(sm[i], silent);
      // check for sign change - indicates root in interval
      log_sil("Left sign: " + leftSign + " right sign: " + rightSign, silent);
      if((leftSign == "-" && rightSign == "+") || (leftSign == "+" && rightSign == "-")) {
        // inject root
        log_sil("Injecting root in interval", silent);
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
        log_sil("No root in interval: taking sign as we go to +inf", silent);
        var m = mapCopy(sm[i].map); mapSet(m, mdp, rightSign);
        newsm.push({map: m, ty: "posinf"});
      }
    } else if(sm[i].ty == "interval") {
      assert(sm[i - 1].ty == "root" && sm[i + 1].ty == "root"); // surrounded by roots
      var leftSign = mapGet(sm[i - 1].map, mdp);
      var rightSign = mapGet(sm[i + 1].map, mdp);
      assert(leftSign != null && rightSign != null);
      // check for sign change - indicates root in interval
      log_sil("Context:", silent);
      printSMrow(sm[i - 1], silent);
      printSMrow(sm[i], silent);
      printSMrow(sm[i + 1], silent);
      log_sil("Left sign: " + leftSign + " right sign: " + rightSign, silent);
      if((leftSign == "-" && rightSign == "+") || (leftSign == "+" && rightSign == "-")) {
        // inject root
        log_sil("Injecting root in interval", silent);
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
        log_sil("No root in interval: taking sign of nonzero endpoint", silent);
        var m = mapCopy(sm[i].map);
        if(leftSign == "0") {
          assert(rightSign != "0");
          mapSet(m, mdp, rightSign);
        } else {
          mapSet(m, mdp, leftSign);
        }
        newsm.push({map: m, ty: "interval"});
      }
    } else if(sm[i].ty == "root") {
      // root signs should already be calculated
      log_sil("Sign at root already calculated", silent);
      var s = mapGet(sm[i].map, mdp);
      assert(s != null);
      var m = mapCopy(sm[i].map)
      newsm.push({map: m, ty: "root"});
    } else {
      throw "illegal row type";
    }
    log_sil("", silent);
  }

  log_sil("Filtering and merging result", silent);

  // final filter
  var retsm = [];
  for(row of newsm) {
    var m = [];
    var isZero = false;
    for(p of polylist) {
      if(mapGet(row.map, p) == "0") {
        isZero = true;
      }
      if(mapGet(row.map, p) == null) {
        isZero = true;
        assert(p.degree() < 0);
        mapSet(m, p, "0");
        continue;
      }
      mapSet(m, p, mapGet(row.map, p));
    }
    if(row.ty != "root" || isZero) {
      retsm.push({map: m, ty: row.ty});
    }
  }

  // final merge
  sm = retsm;
  newsm = [];
  var i = 0;
  while(i < sm.length) {
    l = [];
    while(i < sm.length && (sm[i].ty == "interval" || sm[i].ty == "neginf" || sm[i].ty == "posinf")) {
      l.push({map: mapCopy(sm[i].map), ty: sm[i].ty});
      i++;
    }
    if(l.length == 0) {
      newsm.push({map: mapCopy(sm[i].map), ty: sm[i].ty});
      i++;
      continue;
    } else if(l[0].ty == "neginf" && l[l.length - 1].ty == "posinf") {
      newsm.push({map: l[0].map, ty: "inf"});
    } else if(l[0].ty == "neginf") {
      newsm.push({map: l[0].map, ty: "neginf"});
    } else if(l[l.length - 1].ty == "posinf") {
      newsm.push({map: l[l.length - 1].map, ty: "posinf"});
    } else {
      newsm.push({map: l[0].map, ty: "interval"});
    }
  }
  
  return newsm;
}

function doSMFull() {
  document.getElementById("outputSM").innerHTML = "";
  printRec = document.getElementById("recursePrint").checked;
  pl = document.getElementById("polylist").value.replace(/ /g,'').split(",");
  sm = computeSM(pl.map(x => new Polynomial(x)));
  log("");
  log("FINAL RESULT:");
  printSM(sm, false);
}