/*!
 * @license
 * TradingView Lightweight Charts v3.8.0
 * Copyright (c) 2020 TradingView, Inc.
 * Licensed under Apache License 2.0 https://www.apache.org/licenses/LICENSE-2.0
 */
!(function () {
  "use strict";
  var t, i;
  function n(t, i) {
    var n,
      s = (((n = {})[0] = []),
      (n[1] = [t.lineWidth, t.lineWidth]),
      (n[2] = [2 * t.lineWidth, 2 * t.lineWidth]),
      (n[3] = [6 * t.lineWidth, 6 * t.lineWidth]),
      (n[4] = [t.lineWidth, 4 * t.lineWidth]),
      n)[i];
    t.setLineDash(s);
  }
  function s(t, i, n, s) {
    t.beginPath();
    var h = t.lineWidth % 2 ? 0.5 : 0;
    t.moveTo(n, i + h), t.lineTo(s, i + h), t.stroke();
  }
  function h(t, i) {
    if (!t) throw new Error("Assertion failed" + (i ? ": " + i : ""));
  }
  function r(t) {
    if (void 0 === t) throw new Error("Value is undefined");
    return t;
  }
  function e(t) {
    if (null === t) throw new Error("Value is null");
    return t;
  }
  function u(t) {
    return e(r(t));
  }
  !(function (t) {
    (t[(t.Simple = 0)] = "Simple"), (t[(t.WithSteps = 1)] = "WithSteps");
  })(t || (t = {})),
    (function (t) {
      (t[(t.Solid = 0)] = "Solid"),
        (t[(t.Dotted = 1)] = "Dotted"),
        (t[(t.Dashed = 2)] = "Dashed"),
        (t[(t.LargeDashed = 3)] = "LargeDashed"),
        (t[(t.SparseDotted = 4)] = "SparseDotted");
    })(i || (i = {}));
  var a = {
    khaki: "#f0e68c",
    azure: "#f0ffff",
    aliceblue: "#f0f8ff",
    ghostwhite: "#f8f8ff",
    gold: "#ffd700",
    goldenrod: "#daa520",
    gainsboro: "#dcdcdc",
    gray: "#808080",
    green: "#008000",
    honeydew: "#f0fff0",
    floralwhite: "#fffaf0",
    lightblue: "#add8e6",
    lightcoral: "#f08080",
    lemonchiffon: "#fffacd",
    hotpink: "#ff69b4",
    lightyellow: "#ffffe0",
    greenyellow: "#adff2f",
    lightgoldenrodyellow: "#fafad2",
    limegreen: "#32cd32",
    linen: "#faf0e6",
    lightcyan: "#e0ffff",
    magenta: "#f0f",
    maroon: "#800000",
    olive: "#808000",
    orange: "#ffa500",
    oldlace: "#fdf5e6",
    mediumblue: "#0000cd",
    transparent: "#0000",
    lime: "#0f0",
    lightpink: "#ffb6c1",
    mistyrose: "#ffe4e1",
    moccasin: "#ffe4b5",
    midnightblue: "#191970",
    orchid: "#da70d6",
    mediumorchid: "#ba55d3",
    mediumturquoise: "#48d1cc",
    orangered: "#ff4500",
    royalblue: "#4169e1",
    powderblue: "#b0e0e6",
    red: "#f00",
    coral: "#ff7f50",
    turquoise: "#40e0d0",
    white: "#fff",
    whitesmoke: "#f5f5f5",
    wheat: "#f5deb3",
    teal: "#008080",
    steelblue: "#4682b4",
    bisque: "#ffe4c4",
    aquamarine: "#7fffd4",
    aqua: "#0ff",
    sienna: "#a0522d",
    silver: "#c0c0c0",
    springgreen: "#00ff7f",
    antiquewhite: "#faebd7",
    burlywood: "#deb887",
    brown: "#a52a2a",
    beige: "#f5f5dc",
    chocolate: "#d2691e",
    chartreuse: "#7fff00",
    cornflowerblue: "#6495ed",
    cornsilk: "#fff8dc",
    crimson: "#dc143c",
    cadetblue: "#5f9ea0",
    tomato: "#ff6347",
    fuchsia: "#f0f",
    blue: "#00f",
    salmon: "#fa8072",
    blanchedalmond: "#ffebcd",
    slateblue: "#6a5acd",
    slategray: "#708090",
    thistle: "#d8bfd8",
    tan: "#d2b48c",
    cyan: "#0ff",
    darkblue: "#00008b",
    darkcyan: "#008b8b",
    darkgoldenrod: "#b8860b",
    darkgray: "#a9a9a9",
    blueviolet: "#8a2be2",
    black: "#000",
    darkmagenta: "#8b008b",
    darkslateblue: "#483d8b",
    darkkhaki: "#bdb76b",
    darkorchid: "#9932cc",
    darkorange: "#ff8c00",
    darkgreen: "#006400",
    darkred: "#8b0000",
    dodgerblue: "#1e90ff",
    darkslategray: "#2f4f4f",
    dimgray: "#696969",
    deepskyblue: "#00bfff",
    firebrick: "#b22222",
    forestgreen: "#228b22",
    indigo: "#4b0082",
    ivory: "#fffff0",
    lavenderblush: "#fff0f5",
    feldspar: "#d19275",
    indianred: "#cd5c5c",
    lightgreen: "#90ee90",
    lightgrey: "#d3d3d3",
    lightskyblue: "#87cefa",
    lightslategray: "#789",
    lightslateblue: "#8470ff",
    snow: "#fffafa",
    lightseagreen: "#20b2aa",
    lightsalmon: "#ffa07a",
    darksalmon: "#e9967a",
    darkviolet: "#9400d3",
    mediumpurple: "#9370d8",
    mediumaquamarine: "#66cdaa",
    skyblue: "#87ceeb",
    lavender: "#e6e6fa",
    lightsteelblue: "#b0c4de",
    mediumvioletred: "#c71585",
    mintcream: "#f5fffa",
    navajowhite: "#ffdead",
    navy: "#000080",
    olivedrab: "#6b8e23",
    palevioletred: "#d87093",
    violetred: "#d02090",
    yellow: "#ff0",
    yellowgreen: "#9acd32",
    lawngreen: "#7cfc00",
    pink: "#ffc0cb",
    paleturquoise: "#afeeee",
    palegoldenrod: "#eee8aa",
    darkolivegreen: "#556b2f",
    darkseagreen: "#8fbc8f",
    darkturquoise: "#00ced1",
    peachpuff: "#ffdab9",
    deeppink: "#ff1493",
    violet: "#ee82ee",
    palegreen: "#98fb98",
    mediumseagreen: "#3cb371",
    peru: "#cd853f",
    saddlebrown: "#8b4513",
    sandybrown: "#f4a460",
    rosybrown: "#bc8f8f",
    purple: "#800080",
    seagreen: "#2e8b57",
    seashell: "#fff5ee",
    papayawhip: "#ffefd5",
    mediumslateblue: "#7b68ee",
    plum: "#dda0dd",
    mediumspringgreen: "#00fa9a",
  };
  function o(t) {
    return t < 0 ? 0 : t > 255 ? 255 : Math.round(t) || 0;
  }
  function l(t) {
    return t <= 0 || t > 0
      ? t < 0
        ? 0
        : t > 1
        ? 1
        : Math.round(1e4 * t) / 1e4
      : 0;
  }
  var f = /^#([0-9a-f])([0-9a-f])([0-9a-f])([0-9a-f])?$/i,
    c = /^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})?$/i,
    v = /^rgb\(\s*(-?\d{1,10})\s*,\s*(-?\d{1,10})\s*,\s*(-?\d{1,10})\s*\)$/,
    _ =
      /^rgba\(\s*(-?\d{1,10})\s*,\s*(-?\d{1,10})\s*,\s*(-?\d{1,10})\s*,\s*(-?[\d]{0,10}(?:\.\d+)?)\s*\)$/;
  function d(t) {
    var i;
    if (
      ((t = t.toLowerCase()) in a && (t = a[t]), (i = _.exec(t) || v.exec(t)))
    )
      return [
        o(parseInt(i[1], 10)),
        o(parseInt(i[2], 10)),
        o(parseInt(i[3], 10)),
        l(i.length < 5 ? 1 : parseFloat(i[4])),
      ];
    if ((i = c.exec(t)))
      return [
        o(parseInt(i[1], 16)),
        o(parseInt(i[2], 16)),
        o(parseInt(i[3], 16)),
        1,
      ];
    if ((i = f.exec(t)))
      return [
        o(17 * parseInt(i[1], 16)),
        o(17 * parseInt(i[2], 16)),
        o(17 * parseInt(i[3], 16)),
        1,
      ];
    throw new Error("Cannot parse color: ".concat(t));
  }
  function w(t) {
    var i,
      n = d(t);
    return {
      t: "rgb(".concat(n[0], ", ").concat(n[1], ", ").concat(n[2], ")"),
      i:
        ((i = n),
        0.199 * i[0] + 0.687 * i[1] + 0.114 * i[2] > 160 ? "black" : "white"),
    };
  }
  var M = function (t, i) {
    return (
      (M =
        Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array &&
          function (t, i) {
            t.__proto__ = i;
          }) ||
        function (t, i) {
          for (var n in i)
            Object.prototype.hasOwnProperty.call(i, n) && (t[n] = i[n]);
        }),
      M(t, i)
    );
  };
  function b(t, i) {
    if ("function" != typeof i && null !== i)
      throw new TypeError(
        "Class extends value " + String(i) + " is not a constructor or null"
      );
    function n() {
      this.constructor = t;
    }
    M(t, i),
      (t.prototype =
        null === i ? Object.create(i) : ((n.prototype = i.prototype), new n()));
  }
  var m = function () {
    return (
      (m =
        Object.assign ||
        function (t) {
          for (var i, n = 1, s = arguments.length; n < s; n++)
            for (var h in (i = arguments[n]))
              Object.prototype.hasOwnProperty.call(i, h) && (t[h] = i[h]);
          return t;
        }),
      m.apply(this, arguments)
    );
  };
  function g(t, i, n) {
    if (n || 2 === arguments.length)
      for (var s, h = 0, r = i.length; h < r; h++)
        (!s && h in i) ||
          (s || (s = Array.prototype.slice.call(i, 0, h)), (s[h] = i[h]));
    return t.concat(s || Array.prototype.slice.call(i));
  }
  var p = (function () {
    function t() {
      this.h = [];
    }
    return (
      (t.prototype.u = function (t, i, n) {
        var s = { o: t, l: i, v: !0 === n };
        this.h.push(s);
      }),
      (t.prototype._ = function (t) {
        var i = this.h.findIndex(function (i) {
          return t === i.o;
        });
        i > -1 && this.h.splice(i, 1);
      }),
      (t.prototype.M = function (t) {
        this.h = this.h.filter(function (i) {
          return i.l !== t;
        });
      }),
      (t.prototype.m = function (t, i) {
        var n = g([], this.h, !0);
        (this.h = this.h.filter(function (t) {
          return !t.v;
        })),
          n.forEach(function (n) {
            return n.o(t, i);
          });
      }),
      (t.prototype.g = function () {
        return this.h.length > 0;
      }),
      (t.prototype.p = function () {
        this.h = [];
      }),
      t
    );
  })();
  function y(t) {
    for (var i = [], n = 1; n < arguments.length; n++) i[n - 1] = arguments[n];
    for (var s = 0, h = i; s < h.length; s++) {
      var r = h[s];
      for (var e in r)
        void 0 !== r[e] &&
          ("object" != typeof r[e] || void 0 === t[e]
            ? (t[e] = r[e])
            : y(t[e], r[e]));
    }
    return t;
  }
  function k(t) {
    return "number" == typeof t && isFinite(t);
  }
  function x(t) {
    return "number" == typeof t && t % 1 == 0;
  }
  function N(t) {
    return "string" == typeof t;
  }
  function C(t) {
    return "boolean" == typeof t;
  }
  function S(t) {
    var i,
      n,
      s,
      h = t;
    if (!h || "object" != typeof h) return h;
    for (n in ((i = Array.isArray(h) ? [] : {}), h))
      h.hasOwnProperty(n) &&
        ((s = h[n]), (i[n] = s && "object" == typeof s ? S(s) : s));
    return i;
  }
  function T(t) {
    return null !== t;
  }
  function D(t) {
    return null === t ? void 0 : t;
  }
  var A = "'Trebuchet MS', Roboto, Ubuntu, sans-serif";
  function B(t, i, n) {
    return (
      (n = void 0 !== n ? "".concat(n, " ") : ""),
      void 0 === i && (i = A),
      "".concat(n).concat(t, "px ").concat(i)
    );
  }
  var L = (function () {
      function t(t) {
        (this.k = {
          N: 1,
          C: 4,
          S: NaN,
          T: "",
          D: "",
          A: "",
          B: 0,
          L: 0,
          O: 0,
          F: 0,
          V: 0,
        }),
          (this.P = t);
      }
      return (
        (t.prototype.R = function () {
          var t = this.k,
            i = this.W(),
            n = this.I();
          return (
            (t.S === i && t.D === n) ||
              ((t.S = i),
              (t.D = n),
              (t.T = B(i, n)),
              (t.F = Math.floor(i / 3.5)),
              (t.B = t.F),
              (t.L = Math.max(Math.ceil(i / 2 - t.C / 2), 0)),
              (t.O = Math.ceil(i / 2 + t.C / 2)),
              (t.V = Math.round(i / 10))),
            (t.A = this.j()),
            this.k
          );
        }),
        (t.prototype.j = function () {
          return this.P.R().layout.textColor;
        }),
        (t.prototype.W = function () {
          return this.P.R().layout.fontSize;
        }),
        (t.prototype.I = function () {
          return this.P.R().layout.fontFamily;
        }),
        t
      );
    })(),
    E = (function () {
      function t() {
        this.q = [];
      }
      return (
        (t.prototype.U = function (t) {
          this.q = t;
        }),
        (t.prototype.H = function (t, i, n, s) {
          this.q.forEach(function (h) {
            t.save(), h.H(t, i, n, s), t.restore();
          });
        }),
        t
      );
    })(),
    O = (function () {
      function t() {}
      return (
        (t.prototype.H = function (t, i, n, s) {
          t.save(), t.scale(i, i), this.Y(t, n, s), t.restore();
        }),
        (t.prototype.$ = function (t, i, n, s) {
          t.save(), t.scale(i, i), this.K(t, n, s), t.restore();
        }),
        (t.prototype.K = function (t, i, n) {}),
        t
      );
    })(),
    F = (function (t) {
      function i() {
        var i = (null !== t && t.apply(this, arguments)) || this;
        return (i.X = null), i;
      }
      return (
        b(i, t),
        (i.prototype.Z = function (t) {
          this.X = t;
        }),
        (i.prototype.Y = function (t) {
          if (null !== this.X && null !== this.X.J) {
            var i = this.X.J,
              n = this.X,
              s = function (s) {
                t.beginPath();
                for (var h = i.to - 1; h >= i.from; --h) {
                  var r = n.G[h];
                  t.moveTo(r.tt, r.it), t.arc(r.tt, r.it, s, 0, 2 * Math.PI);
                }
                t.fill();
              };
            (t.fillStyle = n.nt), s(n.st + 2), (t.fillStyle = n.ht), s(n.st);
          }
        }),
        i
      );
    })(O);
  function V() {
    return {
      G: [{ tt: 0, it: 0, rt: 0, et: 0 }],
      ht: "",
      nt: "",
      st: 0,
      J: null,
    };
  }
  var P = { from: 0, to: 1 },
    R = (function () {
      function t(t, i) {
        (this.ut = new E()),
          (this.ot = []),
          (this.lt = []),
          (this.ft = !0),
          (this.P = t),
          (this.ct = i),
          this.ut.U(this.ot);
      }
      return (
        (t.prototype.vt = function (t) {
          var i = this.P._t();
          i.length !== this.ot.length &&
            ((this.lt = i.map(V)),
            (this.ot = this.lt.map(function (t) {
              var i = new F();
              return i.Z(t), i;
            })),
            this.ut.U(this.ot)),
            (this.ft = !0);
        }),
        (t.prototype.dt = function (t, i, n) {
          return this.ft && (this.wt(t), (this.ft = !1)), this.ut;
        }),
        (t.prototype.wt = function (t) {
          var i = this,
            n = this.P._t(),
            s = this.ct.Mt(),
            h = this.P.bt();
          n.forEach(function (n, r) {
            var u,
              a = i.lt[r],
              o = n.gt(s);
            if (null !== o && n.yt()) {
              var l = e(n.kt());
              (a.ht = o.xt),
                (a.st = o.st),
                (a.G[0].et = o.et),
                (a.G[0].it = n.Ct().Nt(o.et, l.St)),
                (a.nt =
                  null !== (u = o.Tt) && void 0 !== u
                    ? u
                    : i.P.Dt(a.G[0].it / t)),
                (a.G[0].rt = s),
                (a.G[0].tt = h.At(s)),
                (a.J = P);
            } else a.J = null;
          });
        }),
        t
      );
    })(),
    z = (function () {
      function t(t) {
        this.Bt = t;
      }
      return (
        (t.prototype.H = function (t, i, h, r) {
          if (null !== this.Bt) {
            var e = this.Bt.Lt.yt,
              u = this.Bt.Et.yt;
            if (e || u) {
              t.save();
              var a = Math.round(this.Bt.tt * i),
                o = Math.round(this.Bt.it * i),
                l = Math.ceil(this.Bt.Ot * i),
                f = Math.ceil(this.Bt.Ft * i);
              (t.lineCap = "butt"),
                e &&
                  a >= 0 &&
                  ((t.lineWidth = Math.floor(this.Bt.Lt.Vt * i)),
                  (t.strokeStyle = this.Bt.Lt.A),
                  (t.fillStyle = this.Bt.Lt.A),
                  n(t, this.Bt.Lt.Pt),
                  (function (t, i, n, s) {
                    t.beginPath();
                    var h = t.lineWidth % 2 ? 0.5 : 0;
                    t.moveTo(i + h, n), t.lineTo(i + h, s), t.stroke();
                  })(t, a, 0, f)),
                u &&
                  o >= 0 &&
                  ((t.lineWidth = Math.floor(this.Bt.Et.Vt * i)),
                  (t.strokeStyle = this.Bt.Et.A),
                  (t.fillStyle = this.Bt.Et.A),
                  n(t, this.Bt.Et.Pt),
                  s(t, o, 0, l)),
                t.restore();
            }
          }
        }),
        t
      );
    })(),
    W = (function () {
      function t(t) {
        (this.ft = !0),
          (this.Rt = {
            Lt: { Vt: 1, Pt: 0, A: "", yt: !1 },
            Et: { Vt: 1, Pt: 0, A: "", yt: !1 },
            Ot: 0,
            Ft: 0,
            tt: 0,
            it: 0,
          }),
          (this.zt = new z(this.Rt)),
          (this.Wt = t);
      }
      return (
        (t.prototype.vt = function () {
          this.ft = !0;
        }),
        (t.prototype.dt = function (t, i) {
          return this.ft && (this.wt(), (this.ft = !1)), this.zt;
        }),
        (t.prototype.wt = function () {
          var t = this.Wt.yt(),
            i = e(this.Wt.It()),
            n = i.jt().R().crosshair,
            s = this.Rt;
          (s.Et.yt = t && this.Wt.qt(i)),
            (s.Lt.yt = t && this.Wt.Ut()),
            (s.Et.Vt = n.horzLine.width),
            (s.Et.Pt = n.horzLine.style),
            (s.Et.A = n.horzLine.color),
            (s.Lt.Vt = n.vertLine.width),
            (s.Lt.Pt = n.vertLine.style),
            (s.Lt.A = n.vertLine.color),
            (s.Ot = i.Ht()),
            (s.Ft = i.Yt()),
            (s.tt = this.Wt.$t()),
            (s.it = this.Wt.Kt());
        }),
        t
      );
    })();
  function I(t, i, n, s, h, r) {
    t.fillRect(i + r, n, s - 2 * r, r),
      t.fillRect(i + r, n + h - r, s - 2 * r, r),
      t.fillRect(i, n, r, h),
      t.fillRect(i + s - r, n, r, h);
  }
  function j(t, i, n) {
    t.save(), t.scale(i, i), n(), t.restore();
  }
  function q(t, i, n, s, h, r) {
    t.save(),
      (t.globalCompositeOperation = "copy"),
      (t.fillStyle = r),
      t.fillRect(i, n, s, h),
      t.restore();
  }
  function U(t, i, n, s, h, r, e) {
    t.save(), (t.globalCompositeOperation = "copy");
    var u = t.createLinearGradient(0, 0, 0, h);
    u.addColorStop(0, r),
      u.addColorStop(1, e),
      (t.fillStyle = u),
      t.fillRect(i, n, s, h),
      t.restore();
  }
  var H,
    Y = (function () {
      function t(t, i) {
        this.Z(t, i);
      }
      return (
        (t.prototype.Z = function (t, i) {
          (this.Bt = t), (this.Xt = i);
        }),
        (t.prototype.H = function (t, i, n, s, h, r) {
          if (this.Bt.yt) {
            t.font = i.T;
            var e = this.Bt.Zt || !this.Bt.Jt ? i.C : 0,
              u = i.N,
              a = i.F,
              o = i.B,
              l = i.L,
              f = i.O,
              c = this.Bt.Gt,
              v = Math.ceil(n.Qt(t, c)),
              _ = i.V,
              d = i.S + a + o,
              w = Math.ceil(0.5 * d),
              M = u + v + l + f + e,
              b = this.Xt.ti;
            this.Xt.ii && (b = this.Xt.ii);
            var m,
              g,
              p = (b = Math.round(b)) - w,
              y = p + d,
              k = "right" === h,
              x = k ? s : 0,
              N = Math.ceil(s * r),
              C = x;
            if (
              ((t.fillStyle = this.Xt.t),
              (t.lineWidth = 1),
              (t.lineCap = "butt"),
              c)
            ) {
              k
                ? ((m = x - e), (g = (C = x - M) + f))
                : ((C = x + M), (m = x + e), (g = x + u + e + l));
              var S = Math.max(1, Math.floor(r)),
                T = Math.max(1, Math.floor(u * r)),
                D = k ? N : 0,
                A = Math.round(p * r),
                B = Math.round(C * r),
                L = Math.round(b * r) - Math.floor(0.5 * r),
                E = L + S + (L - A),
                O = Math.round(m * r);
              t.save(),
                t.beginPath(),
                t.moveTo(D, A),
                t.lineTo(B, A),
                t.lineTo(B, E),
                t.lineTo(D, E),
                t.fill(),
                (t.fillStyle = this.Bt.Tt),
                t.fillRect(k ? N - T : 0, A, T, E - A),
                this.Bt.Zt &&
                  ((t.fillStyle = this.Xt.A), t.fillRect(D, L, O - D, S)),
                (t.textAlign = "left"),
                (t.fillStyle = this.Xt.A),
                j(t, r, function () {
                  t.fillText(c, g, y - o - _);
                }),
                t.restore();
            }
          }
        }),
        (t.prototype.Yt = function (t, i) {
          return this.Bt.yt ? t.S + t.F + t.B : 0;
        }),
        t
      );
    })(),
    $ = (function () {
      function t(t) {
        (this.ni = { ti: 0, A: "#FFF", t: "#000" }),
          (this.si = { Gt: "", yt: !1, Zt: !0, Jt: !1, Tt: "" }),
          (this.hi = { Gt: "", yt: !1, Zt: !1, Jt: !0, Tt: "" }),
          (this.ft = !0),
          (this.ri = new (t || Y)(this.si, this.ni)),
          (this.ei = new (t || Y)(this.hi, this.ni));
      }
      return (
        (t.prototype.Gt = function () {
          return this.ui(), this.si.Gt;
        }),
        (t.prototype.ti = function () {
          return this.ui(), this.ni.ti;
        }),
        (t.prototype.vt = function () {
          this.ft = !0;
        }),
        (t.prototype.Yt = function (t, i) {
          return (
            void 0 === i && (i = !1),
            Math.max(this.ri.Yt(t, i), this.ei.Yt(t, i))
          );
        }),
        (t.prototype.ai = function () {
          return this.ni.ii || 0;
        }),
        (t.prototype.oi = function (t) {
          this.ni.ii = t;
        }),
        (t.prototype.li = function () {
          return this.ui(), this.si.yt || this.hi.yt;
        }),
        (t.prototype.fi = function () {
          return this.ui(), this.si.yt;
        }),
        (t.prototype.dt = function (t) {
          return (
            this.ui(),
            (this.si.Zt = this.si.Zt && t.R().drawTicks),
            (this.hi.Zt = this.hi.Zt && t.R().drawTicks),
            this.ri.Z(this.si, this.ni),
            this.ei.Z(this.hi, this.ni),
            this.ri
          );
        }),
        (t.prototype.ci = function () {
          return (
            this.ui(),
            this.ri.Z(this.si, this.ni),
            this.ei.Z(this.hi, this.ni),
            this.ei
          );
        }),
        (t.prototype.ui = function () {
          this.ft &&
            ((this.si.Zt = !0),
            (this.hi.Zt = !1),
            this.vi(this.si, this.hi, this.ni));
        }),
        t
      );
    })(),
    K = (function (t) {
      function i(i, n, s) {
        var h = t.call(this) || this;
        return (h.Wt = i), (h._i = n), (h.di = s), h;
      }
      return (
        b(i, t),
        (i.prototype.vi = function (t, i, n) {
          t.yt = !1;
          var s = this.Wt.R().horzLine;
          if (s.labelVisible) {
            var h = this._i.kt();
            if (this.Wt.yt() && !this._i.wi() && null !== h) {
              var r = w(s.labelBackgroundColor);
              (n.t = r.t), (n.A = r.i);
              var e = this.di(this._i);
              (n.ti = e.ti), (t.Gt = this._i.Mi(e.et, h)), (t.yt = !0);
            }
          }
        }),
        i
      );
    })($),
    X = /[1-9]/g,
    Z = (function () {
      function t() {
        this.Bt = null;
      }
      return (
        (t.prototype.Z = function (t) {
          this.Bt = t;
        }),
        (t.prototype.H = function (t, i, n) {
          var s = this;
          if (
            null !== this.Bt &&
            !1 !== this.Bt.yt &&
            0 !== this.Bt.Gt.length
          ) {
            t.font = i.T;
            var h = Math.round(i.bi.Qt(t, this.Bt.Gt, X));
            if (!(h <= 0)) {
              t.save();
              var r = i.mi,
                u = h + 2 * r,
                a = u / 2,
                o = this.Bt.Ht,
                l = this.Bt.ti,
                f = Math.floor(l - a) + 0.5;
              f < 0
                ? ((l += Math.abs(0 - f)), (f = Math.floor(l - a) + 0.5))
                : f + u > o &&
                  ((l -= Math.abs(o - (f + u))), (f = Math.floor(l - a) + 0.5));
              var c = f + u,
                v = 0 + i.N + i.F + i.S + i.B;
              t.fillStyle = this.Bt.t;
              var _ = Math.round(f * n),
                d = Math.round(0 * n),
                w = Math.round(c * n),
                M = Math.round(v * n);
              t.fillRect(_, d, w - _, M - d);
              var b = Math.round(this.Bt.ti * n),
                m = d,
                g = Math.round((m + i.N + i.C) * n);
              t.fillStyle = this.Bt.A;
              var p = Math.max(1, Math.floor(n)),
                y = Math.floor(0.5 * n);
              t.fillRect(b - y, m, p, g - m);
              var k = v - i.V - i.B;
              (t.textAlign = "left"),
                (t.fillStyle = this.Bt.A),
                j(t, n, function () {
                  t.fillText(e(s.Bt).Gt, f + r, k);
                }),
                t.restore();
            }
          }
        }),
        t
      );
    })(),
    J = (function () {
      function t(t, i, n) {
        (this.ft = !0),
          (this.zt = new Z()),
          (this.Rt = {
            yt: !1,
            t: "#4c525e",
            A: "white",
            Gt: "",
            Ht: 0,
            ti: NaN,
          }),
          (this.ct = t),
          (this.gi = i),
          (this.di = n);
      }
      return (
        (t.prototype.vt = function () {
          this.ft = !0;
        }),
        (t.prototype.dt = function () {
          return (
            this.ft && (this.wt(), (this.ft = !1)), this.zt.Z(this.Rt), this.zt
          );
        }),
        (t.prototype.wt = function () {
          var t = this.Rt;
          t.yt = !1;
          var i = this.ct.R().vertLine;
          if (i.labelVisible) {
            var n = this.gi.bt();
            if (!n.wi()) {
              var s = n.pi(this.ct.Mt());
              t.Ht = n.Ht();
              var h = this.di();
              if (h.rt) {
                (t.ti = h.ti), (t.Gt = n.yi(e(s))), (t.yt = !0);
                var r = w(i.labelBackgroundColor);
                (t.t = r.t), (t.A = r.i);
              }
            }
          }
        }),
        t
      );
    })(),
    G = (function () {
      function t() {
        (this.ki = null), (this.xi = 0);
      }
      return (
        (t.prototype.Ni = function () {
          return this.xi;
        }),
        (t.prototype.Ci = function (t) {
          this.xi = t;
        }),
        (t.prototype.Ct = function () {
          return this.ki;
        }),
        (t.prototype.Si = function (t) {
          this.ki = t;
        }),
        (t.prototype.Ti = function () {
          return [];
        }),
        (t.prototype.yt = function () {
          return !0;
        }),
        t
      );
    })();
  !(function (t) {
    (t[(t.Normal = 0)] = "Normal"), (t[(t.Magnet = 1)] = "Magnet");
  })(H || (H = {}));
  var Q = (function (t) {
    function i(i, n) {
      var s = t.call(this) || this;
      (s.Di = null),
        (s.Ai = NaN),
        (s.Bi = 0),
        (s.Li = !0),
        (s.Ei = new Map()),
        (s.Oi = !1),
        (s.Fi = NaN),
        (s.Vi = NaN),
        (s.Pi = NaN),
        (s.Ri = NaN),
        (s.gi = i),
        (s.zi = n),
        (s.Wi = new R(i, s));
      var h, r;
      s.Ii =
        ((h = function () {
          return s.Ai;
        }),
        (r = function () {
          return s.Vi;
        }),
        function (t) {
          var i = r(),
            n = h();
          if (t === e(s.Di).ji()) return { et: n, ti: i };
          var u = e(t.kt());
          return { et: t.qi(i, u), ti: i };
        });
      var u = (function (t, i) {
        return function () {
          return { rt: s.gi.bt().pi(t()), ti: i() };
        };
      })(
        function () {
          return s.Bi;
        },
        function () {
          return s.$t();
        }
      );
      return (s.Ui = new J(s, i, u)), (s.Hi = new W(s)), s;
    }
    return (
      b(i, t),
      (i.prototype.R = function () {
        return this.zi;
      }),
      (i.prototype.Yi = function (t, i) {
        (this.Pi = t), (this.Ri = i);
      }),
      (i.prototype.$i = function () {
        (this.Pi = NaN), (this.Ri = NaN);
      }),
      (i.prototype.Ki = function () {
        return this.Pi;
      }),
      (i.prototype.Xi = function () {
        return this.Ri;
      }),
      (i.prototype.Zi = function (t, i, n) {
        this.Oi || (this.Oi = !0), (this.Li = !0), this.Ji(t, i, n);
      }),
      (i.prototype.Mt = function () {
        return this.Bi;
      }),
      (i.prototype.$t = function () {
        return this.Fi;
      }),
      (i.prototype.Kt = function () {
        return this.Vi;
      }),
      (i.prototype.yt = function () {
        return this.Li;
      }),
      (i.prototype.Gi = function () {
        (this.Li = !1),
          this.Qi(),
          (this.Ai = NaN),
          (this.Fi = NaN),
          (this.Vi = NaN),
          (this.Di = null),
          this.$i();
      }),
      (i.prototype.tn = function (t) {
        return null !== this.Di ? [this.Hi, this.Wi] : [];
      }),
      (i.prototype.qt = function (t) {
        return t === this.Di && this.zi.horzLine.visible;
      }),
      (i.prototype.Ut = function () {
        return this.zi.vertLine.visible;
      }),
      (i.prototype.nn = function (t, i) {
        (this.Li && this.Di === t) || this.Ei.clear();
        var n = [];
        return this.Di === t && n.push(this.sn(this.Ei, i, this.Ii)), n;
      }),
      (i.prototype.Ti = function () {
        return this.Li ? [this.Ui] : [];
      }),
      (i.prototype.It = function () {
        return this.Di;
      }),
      (i.prototype.hn = function () {
        this.Hi.vt(),
          this.Ei.forEach(function (t) {
            return t.vt();
          }),
          this.Ui.vt(),
          this.Wi.vt();
      }),
      (i.prototype.rn = function (t) {
        return t && !t.ji().wi() ? t.ji() : null;
      }),
      (i.prototype.Ji = function (t, i, n) {
        this.en(t, i, n) && this.hn();
      }),
      (i.prototype.en = function (t, i, n) {
        var s = this.Fi,
          h = this.Vi,
          r = this.Ai,
          e = this.Bi,
          u = this.Di,
          a = this.rn(n);
        (this.Bi = t),
          (this.Fi = isNaN(t) ? NaN : this.gi.bt().At(t)),
          (this.Di = n);
        var o = null !== a ? a.kt() : null;
        return (
          null !== a && null !== o
            ? ((this.Ai = i), (this.Vi = a.Nt(i, o)))
            : ((this.Ai = NaN), (this.Vi = NaN)),
          s !== this.Fi ||
            h !== this.Vi ||
            e !== this.Bi ||
            r !== this.Ai ||
            u !== this.Di
        );
      }),
      (i.prototype.Qi = function () {
        var t = this.gi
            ._t()
            .map(function (t) {
              return t.an().un();
            })
            .filter(T),
          i = 0 === t.length ? null : Math.max.apply(Math, t);
        this.Bi = null !== i ? i : NaN;
      }),
      (i.prototype.sn = function (t, i, n) {
        var s = t.get(i);
        return void 0 === s && ((s = new K(this, i, n)), t.set(i, s)), s;
      }),
      i
    );
  })(G);
  function tt(t) {
    return "left" === t || "right" === t;
  }
  var it = (function () {
      function t(t) {
        (this.on = new Map()), (this.ln = []), (this.fn = t);
      }
      return (
        (t.prototype.cn = function (t, i) {
          var n = (function (t, i) {
            return void 0 === t
              ? i
              : { vn: Math.max(t.vn, i.vn), _n: t._n || i._n };
          })(this.on.get(t), i);
          this.on.set(t, n);
        }),
        (t.prototype.dn = function () {
          return this.fn;
        }),
        (t.prototype.wn = function (t) {
          var i = this.on.get(t);
          return void 0 === i
            ? { vn: this.fn }
            : { vn: Math.max(this.fn, i.vn), _n: i._n };
        }),
        (t.prototype.Mn = function () {
          this.ln = [{ bn: 0 }];
        }),
        (t.prototype.mn = function (t) {
          this.ln = [{ bn: 1, St: t }];
        }),
        (t.prototype.gn = function () {
          this.ln = [{ bn: 4 }];
        }),
        (t.prototype.pn = function (t) {
          this.ln.push({ bn: 2, St: t });
        }),
        (t.prototype.yn = function (t) {
          this.ln.push({ bn: 3, St: t });
        }),
        (t.prototype.kn = function () {
          return this.ln;
        }),
        (t.prototype.xn = function (t) {
          for (var i = this, n = 0, s = t.ln; n < s.length; n++) {
            var h = s[n];
            this.Nn(h);
          }
          (this.fn = Math.max(this.fn, t.fn)),
            t.on.forEach(function (t, n) {
              i.cn(n, t);
            });
        }),
        (t.prototype.Nn = function (t) {
          switch (t.bn) {
            case 0:
              this.Mn();
              break;
            case 1:
              this.mn(t.St);
              break;
            case 2:
              this.pn(t.St);
              break;
            case 3:
              this.yn(t.St);
              break;
            case 4:
              this.gn();
          }
        }),
        t
      );
    })(),
    nt = ".";
  function st(t, i) {
    if (!k(t)) return "n/a";
    if (!x(i)) throw new TypeError("invalid length");
    if (i < 0 || i > 16) throw new TypeError("invalid length");
    if (0 === i) return t.toString();
    return ("0000000000000000" + t.toString()).slice(-i);
  }
  var ht = (function () {
      function t(t, i) {
        if ((i || (i = 1), (k(t) && x(t)) || (t = 100), t < 0))
          throw new TypeError("invalid base");
        (this._i = t), (this.Cn = i), this.Sn();
      }
      return (
        (t.prototype.format = function (t) {
          var i = t < 0 ? "−" : "";
          return (t = Math.abs(t)), i + this.Tn(t);
        }),
        (t.prototype.Sn = function () {
          if (((this.Dn = 0), this._i > 0 && this.Cn > 0))
            for (var t = this._i; t > 1; ) (t /= 10), this.Dn++;
        }),
        (t.prototype.Tn = function (t) {
          var i = this._i / this.Cn,
            n = Math.floor(t),
            s = "",
            h = void 0 !== this.Dn ? this.Dn : NaN;
          if (i > 1) {
            var r = +(Math.round(t * i) - n * i).toFixed(this.Dn);
            r >= i && ((r -= i), (n += 1)),
              (s = nt + st(+r.toFixed(this.Dn) * this.Cn, h));
          } else (n = Math.round(n * i) / i), h > 0 && (s = nt + st(0, h));
          return n.toFixed(0) + s;
        }),
        t
      );
    })(),
    rt = (function (t) {
      function i(i) {
        return void 0 === i && (i = 100), t.call(this, i) || this;
      }
      return (
        b(i, t),
        (i.prototype.format = function (i) {
          return "".concat(t.prototype.format.call(this, i), "%");
        }),
        i
      );
    })(ht),
    et = (function () {
      function t(t) {
        this.An = t;
      }
      return (
        (t.prototype.format = function (t) {
          var i = "";
          return (
            t < 0 && ((i = "-"), (t = -t)),
            t < 995
              ? i + this.Bn(t)
              : t < 999995
              ? i + this.Bn(t / 1e3) + "K"
              : t < 999999995
              ? ((t = 1e3 * Math.round(t / 1e3)), i + this.Bn(t / 1e6) + "M")
              : ((t = 1e6 * Math.round(t / 1e6)), i + this.Bn(t / 1e9) + "B")
          );
        }),
        (t.prototype.Bn = function (t) {
          var i = Math.pow(10, this.An);
          return (
            (t = Math.round(t * i) / i) >= 1e-15 && t < 1
              ? t.toFixed(this.An).replace(/\.?0+$/, "")
              : String(t)
          ).replace(/(\.[1-9]*)0+$/, function (t, i) {
            return i;
          });
        }),
        t
      );
    })();
  function ut(t, i, n, s) {
    if (0 !== i.length) {
      var h = i[s.from].tt,
        r = i[s.from].it;
      t.moveTo(h, r);
      for (var e = s.from + 1; e < s.to; ++e) {
        var u = i[e];
        if (1 === n) {
          var a = i[e - 1].it,
            o = u.tt;
          t.lineTo(o, a);
        }
        t.lineTo(u.tt, u.it);
      }
    }
  }
  var at = (function (t) {
      function i() {
        var i = (null !== t && t.apply(this, arguments)) || this;
        return (i.X = null), i;
      }
      return (
        b(i, t),
        (i.prototype.Z = function (t) {
          this.X = t;
        }),
        (i.prototype.Y = function (t) {
          if (null !== this.X && 0 !== this.X.G.length && null !== this.X.J) {
            if (
              ((t.lineCap = "butt"),
              (t.lineJoin = "round"),
              (t.lineWidth = this.X.Vt),
              n(t, this.X.Pt),
              (t.lineWidth = 1),
              t.beginPath(),
              1 === this.X.G.length)
            ) {
              var i = this.X.G[0],
                s = this.X.Ln / 2;
              t.moveTo(i.tt - s, this.X.En),
                t.lineTo(i.tt - s, i.it),
                t.lineTo(i.tt + s, i.it),
                t.lineTo(i.tt + s, this.X.En);
            } else
              t.moveTo(this.X.G[this.X.J.from].tt, this.X.En),
                t.lineTo(
                  this.X.G[this.X.J.from].tt,
                  this.X.G[this.X.J.from].it
                ),
                ut(t, this.X.G, this.X.On, this.X.J),
                this.X.J.to > this.X.J.from &&
                  (t.lineTo(this.X.G[this.X.J.to - 1].tt, this.X.En),
                  t.lineTo(this.X.G[this.X.J.from].tt, this.X.En));
            t.closePath(), (t.fillStyle = this.Fn(t)), t.fill();
          }
        }),
        i
      );
    })(O),
    ot = (function (t) {
      function i() {
        return (null !== t && t.apply(this, arguments)) || this;
      }
      return (
        b(i, t),
        (i.prototype.Fn = function (t) {
          var i = this.X,
            n = t.createLinearGradient(0, 0, 0, i.Vn);
          return n.addColorStop(0, i.Pn), n.addColorStop(1, i.Rn), n;
        }),
        i
      );
    })(at),
    lt = (function (t) {
      function i() {
        var i = (null !== t && t.apply(this, arguments)) || this;
        return (i.X = null), i;
      }
      return (
        b(i, t),
        (i.prototype.Z = function (t) {
          this.X = t;
        }),
        (i.prototype.Y = function (t) {
          if (null !== this.X && 0 !== this.X.G.length && null !== this.X.J)
            if (
              ((t.lineCap = "butt"),
              (t.lineWidth = this.X.Vt),
              n(t, this.X.Pt),
              (t.strokeStyle = this.zn(t)),
              (t.lineJoin = "round"),
              1 === this.X.G.length)
            ) {
              t.beginPath();
              var i = this.X.G[0];
              t.moveTo(i.tt - this.X.Ln / 2, i.it),
                t.lineTo(i.tt + this.X.Ln / 2, i.it),
                void 0 !== i.A && (t.strokeStyle = i.A),
                t.stroke();
            } else this.Wn(t, this.X);
        }),
        (i.prototype.Wn = function (t, i) {
          t.beginPath(), ut(t, i.G, i.On, i.J), t.stroke();
        }),
        i
      );
    })(O),
    ft = (function (t) {
      function i() {
        return (null !== t && t.apply(this, arguments)) || this;
      }
      return (
        b(i, t),
        (i.prototype.Wn = function (t, i) {
          var n,
            s,
            h = i.G,
            r = i.J,
            e = i.On,
            u = i.ht;
          if (0 !== h.length && null !== r) {
            t.beginPath();
            var a = h[r.from];
            t.moveTo(a.tt, a.it);
            var o = null !== (n = a.A) && void 0 !== n ? n : u;
            t.strokeStyle = o;
            for (
              var l = function (i) {
                  t.stroke(), t.beginPath(), (t.strokeStyle = i), (o = i);
                },
                f = r.from + 1;
              f < r.to;
              ++f
            ) {
              var c = h[f],
                v = h[f - 1],
                _ = null !== (s = c.A) && void 0 !== s ? s : u;
              1 === e &&
                (t.lineTo(c.tt, v.it), _ !== o && (l(_), t.moveTo(c.tt, v.it))),
                t.lineTo(c.tt, c.it),
                1 !== e && _ !== o && (l(_), t.moveTo(c.tt, c.it));
            }
            t.stroke();
          }
        }),
        (i.prototype.zn = function () {
          return this.X.ht;
        }),
        i
      );
    })(lt);
  function ct(t, i, n, s, h) {
    void 0 === s && (s = 0), void 0 === h && (h = t.length);
    for (var r = h - s; 0 < r; ) {
      var e = r >> 1,
        u = s + e;
      n(t[u], i) ? ((s = u + 1), (r -= e + 1)) : (r = e);
    }
    return s;
  }
  function vt(t, i, n, s, h) {
    void 0 === s && (s = 0), void 0 === h && (h = t.length);
    for (var r = h - s; 0 < r; ) {
      var e = r >> 1,
        u = s + e;
      n(i, t[u]) ? (r = e) : ((s = u + 1), (r -= e + 1));
    }
    return s;
  }
  function _t(t, i) {
    return t.rt < i;
  }
  function dt(t, i) {
    return t < i.rt;
  }
  function wt(t, i, n) {
    var s = i.In(),
      h = i.jn(),
      r = ct(t, s, _t),
      e = vt(t, h, dt);
    if (!n) return { from: r, to: e };
    var u = r,
      a = e;
    return (
      r > 0 && r < t.length && t[r].rt >= s && (u = r - 1),
      e > 0 && e < t.length && t[e - 1].rt <= h && (a = e + 1),
      { from: u, to: a }
    );
  }
  var Mt = (function () {
      function t(t, i, n) {
        (this.qn = !0),
          (this.Un = !0),
          (this.Hn = !0),
          (this.Yn = []),
          (this.$n = null),
          (this.Kn = t),
          (this.Xn = i),
          (this.Zn = n);
      }
      return (
        (t.prototype.vt = function (t) {
          (this.qn = !0),
            "data" === t && (this.Un = !0),
            "options" === t && (this.Hn = !0);
        }),
        (t.prototype.Jn = function () {
          this.Un && (this.Gn(), (this.Un = !1)),
            this.qn && (this.Qn(), (this.qn = !1)),
            this.Hn && (this.ts(), (this.Hn = !1));
        }),
        (t.prototype.ns = function () {
          this.$n = null;
        }),
        (t.prototype.Qn = function () {
          var t = this.Kn.Ct(),
            i = this.Xn.bt();
          if ((this.ns(), !i.wi() && !t.wi())) {
            var n = i.ss();
            if (null !== n && 0 !== this.Kn.an().hs()) {
              var s = this.Kn.kt();
              null !== s &&
                ((this.$n = wt(this.Yn, n, this.Zn)), this.rs(t, i, s.St));
            }
          }
        }),
        t
      );
    })(),
    bt = (function (t) {
      function i(i, n) {
        return t.call(this, i, n, !0) || this;
      }
      return (
        b(i, t),
        (i.prototype.rs = function (t, i, n) {
          i.es(this.Yn, D(this.$n)), t.us(this.Yn, n, D(this.$n));
        }),
        (i.prototype.os = function (t, i) {
          return { rt: t, et: i, tt: NaN, it: NaN };
        }),
        (i.prototype.ts = function () {}),
        (i.prototype.Gn = function () {
          var t = this,
            i = this.Kn.ls();
          this.Yn = this.Kn.an()
            .fs()
            .map(function (n) {
              var s = n.St[3];
              return t.cs(n.vs, s, i);
            });
        }),
        i
      );
    })(Mt),
    mt = (function (t) {
      function i(i, n) {
        var s = t.call(this, i, n) || this;
        return (
          (s.zt = new E()),
          (s._s = new ot()),
          (s.ds = new ft()),
          s.zt.U([s._s, s.ds]),
          s
        );
      }
      return (
        b(i, t),
        (i.prototype.dt = function (t, i) {
          if (!this.Kn.yt()) return null;
          var n = this.Kn.R();
          return (
            this.Jn(),
            this._s.Z({
              On: n.lineType,
              G: this.Yn,
              Pt: n.lineStyle,
              Vt: n.lineWidth,
              Pn: n.topColor,
              Rn: n.bottomColor,
              En: t,
              Vn: t,
              J: this.$n,
              Ln: this.Xn.bt().ws(),
            }),
            this.ds.Z({
              On: n.lineType,
              G: this.Yn,
              ht: n.lineColor,
              Pt: n.lineStyle,
              Vt: n.lineWidth,
              J: this.$n,
              Ln: this.Xn.bt().ws(),
            }),
            this.zt
          );
        }),
        (i.prototype.cs = function (t, i) {
          return this.os(t, i);
        }),
        i
      );
    })(bt);
  var gt = (function () {
      function t() {
        (this.Bt = null), (this.Ms = 0), (this.bs = 0);
      }
      return (
        (t.prototype.Z = function (t) {
          this.Bt = t;
        }),
        (t.prototype.H = function (t, i, n, s) {
          if (
            null !== this.Bt &&
            0 !== this.Bt.an.length &&
            null !== this.Bt.J
          ) {
            if (((this.Ms = this.gs(i)), this.Ms >= 2))
              Math.max(1, Math.floor(i)) % 2 != this.Ms % 2 && this.Ms--;
            this.bs = this.Bt.ps ? Math.min(this.Ms, Math.floor(i)) : this.Ms;
            for (
              var h = null,
                r = this.bs <= this.Ms && this.Bt.ws >= Math.floor(1.5 * i),
                e = this.Bt.J.from;
              e < this.Bt.J.to;
              ++e
            ) {
              var u = this.Bt.an[e];
              h !== u.A && ((t.fillStyle = u.A), (h = u.A));
              var a = Math.floor(0.5 * this.bs),
                o = Math.round(u.tt * i),
                l = o - a,
                f = this.bs,
                c = l + f - 1,
                v = Math.min(u.ys, u.ks),
                _ = Math.max(u.ys, u.ks),
                d = Math.round(v * i) - a,
                w = Math.round(_ * i) + a,
                M = Math.max(w - d, this.bs);
              t.fillRect(l, d, f, M);
              var b = Math.ceil(1.5 * this.Ms);
              if (r) {
                if (this.Bt.xs) {
                  var m = o - b,
                    g = Math.max(d, Math.round(u.Ns * i) - a),
                    p = g + f - 1;
                  p > d + M - 1 && (g = (p = d + M - 1) - f + 1),
                    t.fillRect(m, g, l - m, p - g + 1);
                }
                var y = o + b,
                  k = Math.max(d, Math.round(u.Cs * i) - a),
                  x = k + f - 1;
                x > d + M - 1 && (k = (x = d + M - 1) - f + 1),
                  t.fillRect(c + 1, k, y - c, x - k + 1);
              }
            }
          }
        }),
        (t.prototype.gs = function (t) {
          var i = Math.floor(t);
          return Math.max(
            i,
            Math.floor(
              (function (t, i) {
                return Math.floor(0.3 * t * i);
              })(e(this.Bt).ws, t)
            )
          );
        }),
        t
      );
    })(),
    pt = (function (t) {
      function i(i, n) {
        return t.call(this, i, n, !1) || this;
      }
      return (
        b(i, t),
        (i.prototype.rs = function (t, i, n) {
          i.es(this.Yn, D(this.$n)), t.Ss(this.Yn, n, D(this.$n));
        }),
        (i.prototype.Ts = function (t, i, n) {
          return {
            rt: t,
            open: i.St[0],
            high: i.St[1],
            low: i.St[2],
            close: i.St[3],
            tt: NaN,
            Ns: NaN,
            ys: NaN,
            ks: NaN,
            Cs: NaN,
          };
        }),
        (i.prototype.Gn = function () {
          var t = this,
            i = this.Kn.ls();
          this.Yn = this.Kn.an()
            .fs()
            .map(function (n) {
              return t.cs(n.vs, n, i);
            });
        }),
        i
      );
    })(Mt),
    yt = (function (t) {
      function i() {
        var i = (null !== t && t.apply(this, arguments)) || this;
        return (i.zt = new gt()), i;
      }
      return (
        b(i, t),
        (i.prototype.dt = function (t, i) {
          if (!this.Kn.yt()) return null;
          var n = this.Kn.R();
          this.Jn();
          var s = {
            an: this.Yn,
            ws: this.Xn.bt().ws(),
            xs: n.openVisible,
            ps: n.thinBars,
            J: this.$n,
          };
          return this.zt.Z(s), this.zt;
        }),
        (i.prototype.ts = function () {
          var t = this;
          this.Yn.forEach(function (i) {
            i.A = t.Kn.ls().As(i.rt).Ds;
          });
        }),
        (i.prototype.cs = function (t, i, n) {
          return m(m({}, this.Ts(t, i, n)), { A: n.As(t).Ds });
        }),
        i
      );
    })(pt);
  function kt(t, i, n) {
    return Math.min(Math.max(t, i), n);
  }
  function xt(t, i, n) {
    return i - t <= n;
  }
  function Nt(t) {
    return t <= 0 ? NaN : Math.log(t) / Math.log(10);
  }
  function Ct(t) {
    var i = Math.ceil(t);
    return i % 2 != 0 ? i - 1 : i;
  }
  function St(t) {
    var i = Math.ceil(t);
    return i % 2 == 0 ? i - 1 : i;
  }
  var Tt = (function (t) {
      function i() {
        return (null !== t && t.apply(this, arguments)) || this;
      }
      return (
        b(i, t),
        (i.prototype.Fn = function (t) {
          var i = this.X,
            n = t.createLinearGradient(0, 0, 0, i.Vn),
            s = kt(i.En / i.Vn, 0, 1);
          return (
            n.addColorStop(0, i.Bs),
            n.addColorStop(s, i.Ls),
            n.addColorStop(s, i.Es),
            n.addColorStop(1, i.Os),
            n
          );
        }),
        i
      );
    })(at),
    Dt = (function (t) {
      function i() {
        return (null !== t && t.apply(this, arguments)) || this;
      }
      return (
        b(i, t),
        (i.prototype.zn = function (t) {
          var i = this.X,
            n = t.createLinearGradient(0, 0, 0, i.Vn),
            s = kt(i.En / i.Vn, 0, 1);
          return (
            n.addColorStop(0, i.Pn),
            n.addColorStop(s, i.Pn),
            n.addColorStop(s, i.Rn),
            n.addColorStop(1, i.Rn),
            n
          );
        }),
        i
      );
    })(lt),
    At = (function (t) {
      function i(i, n) {
        var s = t.call(this, i, n) || this;
        return (
          (s.Fs = new Tt()),
          (s.Vs = new Dt()),
          (s.ut = new E()),
          s.ut.U([s.Fs, s.Vs]),
          s
        );
      }
      return (
        b(i, t),
        (i.prototype.dt = function (t, i) {
          if (!this.Kn.yt()) return null;
          var n = this.Kn.kt();
          if (null === n) return null;
          var s = this.Kn.R();
          this.Jn();
          var h = this.Kn.Ct().Nt(s.baseValue.price, n.St),
            r = this.Xn.bt().ws();
          return (
            this.Fs.Z({
              G: this.Yn,
              Bs: s.topFillColor1,
              Ls: s.topFillColor2,
              Es: s.bottomFillColor1,
              Os: s.bottomFillColor2,
              Vt: s.lineWidth,
              Pt: s.lineStyle,
              On: 0,
              En: h,
              Vn: t,
              J: this.$n,
              Ln: r,
            }),
            this.Vs.Z({
              G: this.Yn,
              Pn: s.topLineColor,
              Rn: s.bottomLineColor,
              Vt: s.lineWidth,
              Pt: s.lineStyle,
              On: 0,
              En: h,
              Vn: t,
              J: this.$n,
              Ln: r,
            }),
            this.ut
          );
        }),
        (i.prototype.cs = function (t, i) {
          return this.os(t, i);
        }),
        i
      );
    })(bt),
    Bt = (function () {
      function t() {
        (this.Bt = null), (this.Ms = 0);
      }
      return (
        (t.prototype.Z = function (t) {
          this.Bt = t;
        }),
        (t.prototype.H = function (t, i, n, s) {
          if (
            null !== this.Bt &&
            0 !== this.Bt.an.length &&
            null !== this.Bt.J
          ) {
            if (
              ((this.Ms = (function (t, i) {
                if (t >= 2.5 && t <= 4) return Math.floor(3 * i);
                var n =
                    1 - (0.2 * Math.atan(Math.max(4, t) - 4)) / (0.5 * Math.PI),
                  s = Math.floor(t * n * i),
                  h = Math.floor(t * i),
                  r = Math.min(s, h);
                return Math.max(Math.floor(i), r);
              })(this.Bt.ws, i)),
              this.Ms >= 2)
            )
              Math.floor(i) % 2 != this.Ms % 2 && this.Ms--;
            var h = this.Bt.an;
            this.Bt.Ps && this.Rs(t, h, this.Bt.J, i),
              this.Bt.zs && this.Ws(t, h, this.Bt.J, this.Bt.ws, i);
            var r = this.Is(i);
            (!this.Bt.zs || this.Ms > 2 * r) && this.js(t, h, this.Bt.J, i);
          }
        }),
        (t.prototype.Rs = function (t, i, n, s) {
          if (null !== this.Bt) {
            var h = "",
              r = Math.min(Math.floor(s), Math.floor(this.Bt.ws * s));
            r = Math.max(Math.floor(s), Math.min(r, this.Ms));
            for (
              var e = Math.floor(0.5 * r), u = null, a = n.from;
              a < n.to;
              a++
            ) {
              var o = i[a];
              o.qs !== h && ((t.fillStyle = o.qs), (h = o.qs));
              var l = Math.round(Math.min(o.Ns, o.Cs) * s),
                f = Math.round(Math.max(o.Ns, o.Cs) * s),
                c = Math.round(o.ys * s),
                v = Math.round(o.ks * s),
                _ = Math.round(s * o.tt) - e,
                d = _ + r - 1;
              null !== u && ((_ = Math.max(u + 1, _)), (_ = Math.min(_, d)));
              var w = d - _ + 1;
              t.fillRect(_, c, w, l - c),
                t.fillRect(_, f + 1, w, v - f),
                (u = d);
            }
          }
        }),
        (t.prototype.Is = function (t) {
          var i = Math.floor(1 * t);
          this.Ms <= 2 * i && (i = Math.floor(0.5 * (this.Ms - 1)));
          var n = Math.max(Math.floor(t), i);
          return this.Ms <= 2 * n
            ? Math.max(Math.floor(t), Math.floor(1 * t))
            : n;
        }),
        (t.prototype.Ws = function (t, i, n, s, h) {
          if (null !== this.Bt)
            for (
              var r = "", e = this.Is(h), u = null, a = n.from;
              a < n.to;
              a++
            ) {
              var o = i[a];
              o.Tt !== r && ((t.fillStyle = o.Tt), (r = o.Tt));
              var l = Math.round(o.tt * h) - Math.floor(0.5 * this.Ms),
                f = l + this.Ms - 1,
                c = Math.round(Math.min(o.Ns, o.Cs) * h),
                v = Math.round(Math.max(o.Ns, o.Cs) * h);
              if (
                (null !== u && ((l = Math.max(u + 1, l)), (l = Math.min(l, f))),
                this.Bt.ws * h > 2 * e)
              )
                I(t, l, c, f - l + 1, v - c + 1, e);
              else {
                var _ = f - l + 1;
                t.fillRect(l, c, _, v - c + 1);
              }
              u = f;
            }
        }),
        (t.prototype.js = function (t, i, n, s) {
          if (null !== this.Bt)
            for (var h = "", r = this.Is(s), e = n.from; e < n.to; e++) {
              var u = i[e],
                a = Math.round(Math.min(u.Ns, u.Cs) * s),
                o = Math.round(Math.max(u.Ns, u.Cs) * s),
                l = Math.round(u.tt * s) - Math.floor(0.5 * this.Ms),
                f = l + this.Ms - 1;
              if (u.A !== h) {
                var c = u.A;
                (t.fillStyle = c), (h = c);
              }
              this.Bt.zs && ((l += r), (a += r), (f -= r), (o -= r)),
                a > o || t.fillRect(l, a, f - l + 1, o - a + 1);
            }
        }),
        t
      );
    })(),
    Lt = (function (t) {
      function i() {
        var i = (null !== t && t.apply(this, arguments)) || this;
        return (i.zt = new Bt()), i;
      }
      return (
        b(i, t),
        (i.prototype.dt = function (t, i) {
          if (!this.Kn.yt()) return null;
          var n = this.Kn.R();
          this.Jn();
          var s = {
            an: this.Yn,
            ws: this.Xn.bt().ws(),
            Ps: n.wickVisible,
            zs: n.borderVisible,
            J: this.$n,
          };
          return this.zt.Z(s), this.zt;
        }),
        (i.prototype.ts = function () {
          var t = this;
          this.Yn.forEach(function (i) {
            var n = t.Kn.ls().As(i.rt);
            (i.A = n.Ds), (i.qs = n.Us), (i.Tt = n.Hs);
          });
        }),
        (i.prototype.cs = function (t, i, n) {
          var s = n.As(t);
          return m(m({}, this.Ts(t, i, n)), { A: s.Ds, qs: s.Us, Tt: s.Hs });
        }),
        i
      );
    })(pt),
    Et = (function () {
      function t() {
        (this.Bt = null), (this.Ys = []);
      }
      return (
        (t.prototype.Z = function (t) {
          (this.Bt = t), (this.Ys = []);
        }),
        (t.prototype.H = function (t, i, n, s) {
          if (
            null !== this.Bt &&
            0 !== this.Bt.G.length &&
            null !== this.Bt.J
          ) {
            this.Ys.length || this.$s(i);
            for (
              var h = Math.max(1, Math.floor(i)),
                r = Math.round(this.Bt.Ks * i) - Math.floor(h / 2),
                e = r + h,
                u = this.Bt.J.from;
              u < this.Bt.J.to;
              u++
            ) {
              var a = this.Bt.G[u],
                o = this.Ys[u - this.Bt.J.from],
                l = Math.round(a.it * i);
              t.fillStyle = a.A;
              var f = void 0,
                c = void 0;
              l <= r
                ? ((f = l), (c = e))
                : ((f = r), (c = l - Math.floor(h / 2) + h)),
                t.fillRect(o.In, f, o.jn - o.In + 1, c - f);
            }
          }
        }),
        (t.prototype.$s = function (t) {
          if (
            null !== this.Bt &&
            0 !== this.Bt.G.length &&
            null !== this.Bt.J
          ) {
            var i =
                Math.ceil(this.Bt.ws * t) <= 1 ? 0 : Math.max(1, Math.floor(t)),
              n = Math.round(this.Bt.ws * t) - i;
            this.Ys = new Array(this.Bt.J.to - this.Bt.J.from);
            for (var s = this.Bt.J.from; s < this.Bt.J.to; s++) {
              var h,
                r = this.Bt.G[s],
                e = Math.round(r.tt * t),
                u = void 0,
                a = void 0;
              if (n % 2) (u = e - (h = (n - 1) / 2)), (a = e + h);
              else (u = e - (h = n / 2)), (a = e + h - 1);
              this.Ys[s - this.Bt.J.from] = {
                In: u,
                jn: a,
                Xs: e,
                Zs: r.tt * t,
                rt: r.rt,
              };
            }
            for (s = this.Bt.J.from + 1; s < this.Bt.J.to; s++) {
              var o = this.Ys[s - this.Bt.J.from],
                l = this.Ys[s - this.Bt.J.from - 1];
              o.rt === l.rt + 1 &&
                o.In - l.jn !== i + 1 &&
                (l.Xs > l.Zs ? (l.jn = o.In - i - 1) : (o.In = l.jn + i + 1));
            }
            var f = Math.ceil(this.Bt.ws * t);
            for (s = this.Bt.J.from; s < this.Bt.J.to; s++) {
              (o = this.Ys[s - this.Bt.J.from]).jn < o.In && (o.jn = o.In);
              var c = o.jn - o.In + 1;
              f = Math.min(c, f);
            }
            if (i > 0 && f < 4)
              for (s = this.Bt.J.from; s < this.Bt.J.to; s++) {
                (c = (o = this.Ys[s - this.Bt.J.from]).jn - o.In + 1) > f &&
                  (o.Xs > o.Zs ? (o.jn -= 1) : (o.In += 1));
              }
          } else this.Ys = [];
        }),
        t
      );
    })();
  function Ot(t) {
    return { G: [], ws: t, Ks: NaN, J: null };
  }
  function Ft(t, i, n) {
    return { rt: t, et: i, tt: NaN, it: NaN, A: n };
  }
  var Vt = (function (t) {
      function i(i, n) {
        var s = t.call(this, i, n, !1) || this;
        return (s.ut = new E()), (s.Js = Ot(0)), (s.zt = new Et()), s;
      }
      return (
        b(i, t),
        (i.prototype.dt = function (t, i) {
          return this.Kn.yt() ? (this.Jn(), this.ut) : null;
        }),
        (i.prototype.Gn = function () {
          var t = this.Xn.bt().ws();
          this.Js = Ot(t);
          for (
            var i = 0,
              n = 0,
              s = this.Kn.R().color,
              h = 0,
              r = this.Kn.an().fs();
            h < r.length;
            h++
          ) {
            var e = r[h],
              u = e.St[3],
              a = void 0 !== e.A ? e.A : s,
              o = Ft(e.vs, u, a);
            ++i < this.Js.G.length ? (this.Js.G[i] = o) : this.Js.G.push(o),
              (this.Yn[n++] = { rt: e.vs, tt: 0 });
          }
          this.zt.Z(this.Js), this.ut.U([this.zt]);
        }),
        (i.prototype.ts = function () {}),
        (i.prototype.ns = function () {
          t.prototype.ns.call(this), (this.Js.J = null);
        }),
        (i.prototype.rs = function (t, i, n) {
          if (null !== this.$n) {
            var s = i.ws(),
              h = e(i.ss()),
              r = t.Nt(this.Kn.R().base, n);
            i.es(this.Js.G),
              t.us(this.Js.G, n),
              (this.Js.Ks = r),
              (this.Js.J = wt(this.Js.G, h, !1)),
              (this.Js.ws = s),
              this.zt.Z(this.Js);
          }
        }),
        i
      );
    })(Mt),
    Pt = (function (t) {
      function i(i, n) {
        var s = t.call(this, i, n) || this;
        return (s.ds = new ft()), s;
      }
      return (
        b(i, t),
        (i.prototype.dt = function (t, i) {
          if (!this.Kn.yt()) return null;
          var n = this.Kn.R();
          this.Jn();
          var s = {
            G: this.Yn,
            ht: n.color,
            Pt: n.lineStyle,
            On: n.lineType,
            Vt: n.lineWidth,
            J: this.$n,
            Ln: this.Xn.bt().ws(),
          };
          return this.ds.Z(s), this.ds;
        }),
        (i.prototype.ts = function () {
          var t = this;
          this.Yn.forEach(function (i) {
            i.A = t.Kn.ls().As(i.rt).Ds;
          });
        }),
        (i.prototype.cs = function (t, i, n) {
          var s = this.os(t, i);
          return (s.A = n.As(t).Ds), s;
        }),
        i
      );
    })(bt),
    Rt = /[2-9]/g,
    zt = (function () {
      function t(t) {
        void 0 === t && (t = 50),
          (this.Gs = new Map()),
          (this.Qs = 0),
          (this.th = Array.from(new Array(t)));
      }
      return (
        (t.prototype.ih = function () {
          this.Gs.clear(), this.th.fill(void 0);
        }),
        (t.prototype.Qt = function (t, i, n) {
          var s = n || Rt,
            h = String(i).replace(s, "0"),
            r = this.Gs.get(h);
          if (void 0 === r) {
            if (0 === (r = t.measureText(h).width) && 0 !== i.length) return 0;
            var e = this.th[this.Qs];
            void 0 !== e && this.Gs.delete(e),
              (this.th[this.Qs] = h),
              (this.Qs = (this.Qs + 1) % this.th.length),
              this.Gs.set(h, r);
          }
          return r;
        }),
        t
      );
    })(),
    Wt = (function () {
      function t(t) {
        (this.nh = null),
          (this.k = null),
          (this.sh = "right"),
          (this.hh = 0),
          (this.rh = t);
      }
      return (
        (t.prototype.eh = function (t, i, n, s) {
          (this.nh = t), (this.k = i), (this.hh = n), (this.sh = s);
        }),
        (t.prototype.H = function (t, i) {
          null !== this.k &&
            null !== this.nh &&
            this.nh.H(t, this.k, this.rh, this.hh, this.sh, i);
        }),
        t
      );
    })(),
    It = (function () {
      function t(t, i, n) {
        (this.uh = t),
          (this.rh = new zt(50)),
          (this.ah = i),
          (this.P = n),
          (this.W = -1),
          (this.zt = new Wt(this.rh));
      }
      return (
        (t.prototype.dt = function (t, i) {
          var n = this.P.oh(this.ah);
          if (null === n) return null;
          var s = n.lh(this.ah) ? n.fh() : this.ah.Ct();
          if (null === s) return null;
          var h = n._h(s);
          if ("overlay" === h) return null;
          var r = this.P.dh();
          return (
            r.S !== this.W && ((this.W = r.S), this.rh.ih()),
            this.zt.eh(this.uh.ci(), r, i, h),
            this.zt
          );
        }),
        t
      );
    })(),
    jt = (function () {
      function t() {
        this.Bt = null;
      }
      return (
        (t.prototype.Z = function (t) {
          this.Bt = t;
        }),
        (t.prototype.H = function (t, i, h, r) {
          if (null !== this.Bt && !1 !== this.Bt.yt) {
            var e = Math.round(this.Bt.it * i);
            if (!(e < 0 || e > Math.ceil(this.Bt.Yt * i))) {
              var u = Math.ceil(this.Bt.Ht * i);
              (t.lineCap = "butt"),
                (t.strokeStyle = this.Bt.A),
                (t.lineWidth = Math.floor(this.Bt.Vt * i)),
                n(t, this.Bt.Pt),
                s(t, e, 0, u);
            }
          }
        }),
        t
      );
    })(),
    qt = (function () {
      function t(t) {
        (this.wh = {
          Ht: 0,
          Yt: 0,
          it: 0,
          A: "rgba(0, 0, 0, 0)",
          Vt: 1,
          Pt: 0,
          yt: !1,
        }),
          (this.Mh = new jt()),
          (this.ft = !0),
          (this.Kn = t),
          (this.Xn = t.jt()),
          this.Mh.Z(this.wh);
      }
      return (
        (t.prototype.vt = function () {
          this.ft = !0;
        }),
        (t.prototype.dt = function (t, i) {
          return this.Kn.yt()
            ? (this.ft && (this.bh(t, i), (this.ft = !1)), this.Mh)
            : null;
        }),
        t
      );
    })(),
    Ut = (function (t) {
      function i(i) {
        return t.call(this, i) || this;
      }
      return (
        b(i, t),
        (i.prototype.bh = function (t, i) {
          this.wh.yt = !1;
          var n = this.Kn.Ct(),
            s = n.mh().mh;
          if (2 === s || 3 === s) {
            var h = this.Kn.R();
            if (h.baseLineVisible && this.Kn.yt()) {
              var r = this.Kn.kt();
              null !== r &&
                ((this.wh.yt = !0),
                (this.wh.it = n.Nt(r.St, r.St)),
                (this.wh.Ht = i),
                (this.wh.Yt = t),
                (this.wh.A = h.baseLineColor),
                (this.wh.Vt = h.baseLineWidth),
                (this.wh.Pt = h.baseLineStyle));
            }
          }
        }),
        i
      );
    })(qt),
    Ht = (function () {
      function t() {
        this.Bt = null;
      }
      return (
        (t.prototype.Z = function (t) {
          this.Bt = t;
        }),
        (t.prototype.gh = function () {
          return this.Bt;
        }),
        (t.prototype.H = function (t, i, n, s) {
          var h = this.Bt;
          if (null !== h) {
            t.save();
            var r = Math.max(1, Math.floor(i)),
              e = (r % 2) / 2,
              u = Math.round(h.Zs.x * i) + e,
              a = h.Zs.y * i;
            (t.fillStyle = h.ph), t.beginPath();
            var o = Math.max(2, 1.5 * h.yh) * i;
            t.arc(u, a, o, 0, 2 * Math.PI, !1),
              t.fill(),
              (t.fillStyle = h.kh),
              t.beginPath(),
              t.arc(u, a, h.st * i, 0, 2 * Math.PI, !1),
              t.fill(),
              (t.lineWidth = r),
              (t.strokeStyle = h.xh),
              t.beginPath(),
              t.arc(u, a, h.st * i + r / 2, 0, 2 * Math.PI, !1),
              t.stroke(),
              t.restore();
          }
        }),
        t
      );
    })(),
    Yt = [
      { Nh: 0, Ch: 0.25, Sh: 4, Th: 10, Dh: 0.25, Ah: 0, Bh: 0.4, Lh: 0.8 },
      { Nh: 0.25, Ch: 0.525, Sh: 10, Th: 14, Dh: 0, Ah: 0, Bh: 0.8, Lh: 0 },
      { Nh: 0.525, Ch: 1, Sh: 14, Th: 14, Dh: 0, Ah: 0, Bh: 0, Lh: 0 },
    ];
  function $t(t, i, n, s) {
    return (function (t, i) {
      if ("transparent" === t) return t;
      var n = d(t),
        s = n[3];
      return "rgba("
        .concat(n[0], ", ")
        .concat(n[1], ", ")
        .concat(n[2], ", ")
        .concat(i * s, ")");
    })(t, n + (s - n) * i);
  }
  function Kt(t, i) {
    for (var n, s = (t % 2600) / 2600, r = 0, e = Yt; r < e.length; r++) {
      var u = e[r];
      if (s >= u.Nh && s <= u.Ch) {
        n = u;
        break;
      }
    }
    h(void 0 !== n, "Last price animation internal logic error");
    var a,
      o,
      l,
      f = (s - n.Nh) / (n.Ch - n.Nh);
    return {
      kh: $t(i, f, n.Dh, n.Ah),
      xh: $t(i, f, n.Bh, n.Lh),
      st: ((a = f), (o = n.Sh), (l = n.Th), o + (l - o) * a),
    };
  }
  var Xt = (function () {
    function t(t) {
      (this.zt = new Ht()),
        (this.ft = !0),
        (this.Eh = !0),
        (this.Oh = performance.now()),
        (this.Fh = this.Oh - 1),
        (this.Vh = t);
    }
    return (
      (t.prototype.Ph = function () {
        (this.Fh = this.Oh - 1), this.vt();
      }),
      (t.prototype.Rh = function () {
        if ((this.vt(), 2 === this.Vh.R().lastPriceAnimation)) {
          var t = performance.now(),
            i = this.Fh - t;
          if (i > 0) return void (i < 650 && (this.Fh += 2600));
          (this.Oh = t), (this.Fh = t + 2600);
        }
      }),
      (t.prototype.vt = function () {
        this.ft = !0;
      }),
      (t.prototype.zh = function () {
        this.Eh = !0;
      }),
      (t.prototype.yt = function () {
        return 0 !== this.Vh.R().lastPriceAnimation;
      }),
      (t.prototype.Wh = function () {
        switch (this.Vh.R().lastPriceAnimation) {
          case 0:
            return !1;
          case 1:
            return !0;
          case 2:
            return performance.now() <= this.Fh;
        }
      }),
      (t.prototype.dt = function (t, i) {
        return (
          this.ft
            ? (this.wt(t, i), (this.ft = !1), (this.Eh = !1))
            : this.Eh && (this.Ih(), (this.Eh = !1)),
          this.zt
        );
      }),
      (t.prototype.wt = function (t, i) {
        this.zt.Z(null);
        var n = this.Vh.jt().bt(),
          s = n.ss(),
          h = this.Vh.kt();
        if (null !== s && null !== h) {
          var r = this.Vh.jh(!0);
          if (!r.qh && s.Uh(r.vs)) {
            var e = { x: n.At(r.vs), y: this.Vh.Ct().Nt(r.et, h.St) },
              u = r.A,
              a = this.Vh.R().lineWidth,
              o = Kt(this.Hh(), u);
            this.zt.Z({ ph: u, yh: a, kh: o.kh, xh: o.xh, st: o.st, Zs: e });
          }
        }
      }),
      (t.prototype.Ih = function () {
        var t = this.zt.gh();
        if (null !== t) {
          var i = Kt(this.Hh(), t.ph);
          (t.kh = i.kh), (t.xh = i.xh), (t.st = i.st);
        }
      }),
      (t.prototype.Hh = function () {
        return this.Wh() ? performance.now() - this.Oh : 2599;
      }),
      t
    );
  })();
  function Zt(t, i) {
    return St(Math.min(Math.max(t, 12), 30) * i);
  }
  function Jt(t, i) {
    switch (t) {
      case "arrowDown":
      case "arrowUp":
        return Zt(i, 1);
      case "circle":
        return Zt(i, 0.8);
      case "square":
        return Zt(i, 0.7);
    }
  }
  function Gt(t) {
    return Ct(Zt(t, 1));
  }
  function Qt(t) {
    return Math.max(Zt(t, 0.1), 3);
  }
  function ti(t, i, n, s, h) {
    var r = Jt("square", n),
      e = (r - 1) / 2,
      u = t - e,
      a = i - e;
    return s >= u && s <= u + r && h >= a && h <= a + r;
  }
  function ii(t, i, n, s, h) {
    var r = (Jt("arrowUp", h) - 1) / 2,
      e = (St(h / 2) - 1) / 2;
    i.beginPath(),
      t
        ? (i.moveTo(n - r, s),
          i.lineTo(n, s - r),
          i.lineTo(n + r, s),
          i.lineTo(n + e, s),
          i.lineTo(n + e, s + r),
          i.lineTo(n - e, s + r),
          i.lineTo(n - e, s))
        : (i.moveTo(n - r, s),
          i.lineTo(n, s + r),
          i.lineTo(n + r, s),
          i.lineTo(n + e, s),
          i.lineTo(n + e, s - r),
          i.lineTo(n - e, s - r),
          i.lineTo(n - e, s)),
      i.fill();
  }
  function ni(t, i, n, s, h, r) {
    return ti(i, n, s, h, r);
  }
  var si = (function (t) {
    function i() {
      var i = (null !== t && t.apply(this, arguments)) || this;
      return (
        (i.Bt = null), (i.rh = new zt()), (i.W = -1), (i.I = ""), (i.Yh = ""), i
      );
    }
    return (
      b(i, t),
      (i.prototype.Z = function (t) {
        this.Bt = t;
      }),
      (i.prototype.eh = function (t, i) {
        (this.W === t && this.I === i) ||
          ((this.W = t), (this.I = i), (this.Yh = B(t, i)), this.rh.ih());
      }),
      (i.prototype.$h = function (t, i) {
        if (null === this.Bt || null === this.Bt.J) return null;
        for (var n = this.Bt.J.from; n < this.Bt.J.to; n++) {
          var s = this.Bt.G[n];
          if (ri(s, t, i)) return { Kh: s.Xh, Zh: s.Zh };
        }
        return null;
      }),
      (i.prototype.Y = function (t, i, n) {
        if (null !== this.Bt && null !== this.Bt.J) {
          (t.textBaseline = "middle"), (t.font = this.Yh);
          for (var s = this.Bt.J.from; s < this.Bt.J.to; s++) {
            var h = this.Bt.G[s];
            void 0 !== h.Gt &&
              ((h.Gt.Ht = this.rh.Qt(t, h.Gt.Jh)), (h.Gt.Yt = this.W)),
              hi(h, t);
          }
        }
      }),
      i
    );
  })(O);
  function hi(t, i) {
    (i.fillStyle = t.A),
      void 0 !== t.Gt &&
        (function (t, i, n, s) {
          t.fillText(i, n, s);
        })(i, t.Gt.Jh, t.tt - t.Gt.Ht / 2, t.Gt.it),
      (function (t, i) {
        if (0 === t.hs) return;
        switch (t.Gh) {
          case "arrowDown":
            return void ii(!1, i, t.tt, t.it, t.hs);
          case "arrowUp":
            return void ii(!0, i, t.tt, t.it, t.hs);
          case "circle":
            return void (function (t, i, n, s) {
              var h = (Jt("circle", s) - 1) / 2;
              t.beginPath(), t.arc(i, n, h, 0, 2 * Math.PI, !1), t.fill();
            })(i, t.tt, t.it, t.hs);
          case "square":
            return void (function (t, i, n, s) {
              var h = Jt("square", s),
                r = (h - 1) / 2,
                e = i - r,
                u = n - r;
              t.fillRect(e, u, h, h);
            })(i, t.tt, t.it, t.hs);
        }
        t.Gh;
      })(t, i);
  }
  function ri(t, i, n) {
    return (
      !(
        void 0 === t.Gt ||
        !(function (t, i, n, s, h, r) {
          var e = s / 2;
          return h >= t && h <= t + n && r >= i - e && r <= i + e;
        })(t.tt, t.Gt.it, t.Gt.Ht, t.Gt.Yt, i, n)
      ) ||
      (function (t, i, n) {
        if (0 === t.hs) return !1;
        switch (t.Gh) {
          case "arrowDown":
          case "arrowUp":
            return ni(0, t.tt, t.it, t.hs, i, n);
          case "circle":
            return (function (t, i, n, s, h) {
              var r = 2 + Jt("circle", n) / 2,
                e = t - s,
                u = i - h;
              return Math.sqrt(e * e + u * u) <= r;
            })(t.tt, t.it, t.hs, i, n);
          case "square":
            return ti(t.tt, t.it, t.hs, i, n);
        }
      })(t, i, n)
    );
  }
  function ei(t, i, n, s, h, r, e, u, a) {
    var o = k(n) ? n : n.close,
      l = k(n) ? n : n.high,
      f = k(n) ? n : n.low,
      c = k(i.size) ? Math.max(i.size, 0) : 1,
      v = Gt(u.ws()) * c,
      _ = v / 2;
    switch (((t.hs = v), i.position)) {
      case "inBar":
        return (
          (t.it = e.Nt(o, a)),
          void (void 0 !== t.Gt && (t.Gt.it = t.it + _ + r + 0.6 * h))
        );
      case "aboveBar":
        return (
          (t.it = e.Nt(l, a) - _ - s.Qh),
          void 0 !== t.Gt &&
            ((t.Gt.it = t.it - _ - 0.6 * h), (s.Qh += 1.2 * h)),
          void (s.Qh += v + r)
        );
      case "belowBar":
        return (
          (t.it = e.Nt(f, a) + _ + s.tr),
          void 0 !== t.Gt &&
            ((t.Gt.it = t.it + _ + r + 0.6 * h), (s.tr += 1.2 * h)),
          void (s.tr += v + r)
        );
    }
    i.position;
  }
  var ui = (function () {
      function t(t, i) {
        (this.ft = !0),
          (this.ir = !0),
          (this.nr = !0),
          (this.sr = null),
          (this.zt = new si()),
          (this.Vh = t),
          (this.gi = i),
          (this.Bt = { G: [], J: null });
      }
      return (
        (t.prototype.vt = function (t) {
          (this.ft = !0), (this.nr = !0), "data" === t && (this.ir = !0);
        }),
        (t.prototype.dt = function (t, i, n) {
          if (!this.Vh.yt()) return null;
          this.ft && this.Jn();
          var s = this.gi.R().layout;
          return (
            this.zt.eh(s.fontSize, s.fontFamily), this.zt.Z(this.Bt), this.zt
          );
        }),
        (t.prototype.hr = function () {
          if (this.nr) {
            if (this.Vh.rr().length > 0) {
              var t = this.gi.bt().ws(),
                i = Qt(t),
                n = 1.5 * Gt(t) + 2 * i;
              this.sr = { above: n, below: n };
            } else this.sr = null;
            this.nr = !1;
          }
          return this.sr;
        }),
        (t.prototype.Jn = function () {
          var t = this.Vh.Ct(),
            i = this.gi.bt(),
            n = this.Vh.rr();
          this.ir &&
            ((this.Bt.G = n.map(function (t) {
              return {
                rt: t.time,
                tt: 0,
                it: 0,
                hs: 0,
                Gh: t.shape,
                A: t.color,
                Xh: t.Xh,
                Zh: t.id,
                Gt: void 0,
              };
            })),
            (this.ir = !1));
          var s = this.gi.R().layout;
          this.Bt.J = null;
          var h = i.ss();
          if (null !== h) {
            var r = this.Vh.kt();
            if (null !== r && 0 !== this.Bt.G.length) {
              var e = NaN,
                u = Qt(i.ws()),
                a = { Qh: u, tr: u };
              this.Bt.J = wt(this.Bt.G, h, !0);
              for (var o = this.Bt.J.from; o < this.Bt.J.to; o++) {
                var l = n[o];
                l.time !== e && ((a.Qh = u), (a.tr = u), (e = l.time));
                var f = this.Bt.G[o];
                (f.tt = i.At(l.time)),
                  void 0 !== l.text &&
                    l.text.length > 0 &&
                    (f.Gt = { Jh: l.text, it: 0, Ht: 0, Yt: 0 });
                var c = this.Vh.er(l.time);
                null !== c && ei(f, l, c, a, s.fontSize, u, t, i, r.St);
              }
              this.ft = !1;
            }
          }
        }),
        t
      );
    })(),
    ai = (function (t) {
      function i(i) {
        return t.call(this, i) || this;
      }
      return (
        b(i, t),
        (i.prototype.bh = function (t, i) {
          var n = this.wh;
          n.yt = !1;
          var s = this.Kn.R();
          if (s.priceLineVisible && this.Kn.yt()) {
            var h = this.Kn.jh(0 === s.priceLineSource);
            h.qh ||
              ((n.yt = !0),
              (n.it = h.ti),
              (n.A = this.Kn.ur(h.A)),
              (n.Ht = i),
              (n.Yt = t),
              (n.Vt = s.priceLineWidth),
              (n.Pt = s.priceLineStyle));
          }
        }),
        i
      );
    })(qt),
    oi = (function (t) {
      function i(i) {
        var n = t.call(this) || this;
        return (n.Wt = i), n;
      }
      return (
        b(i, t),
        (i.prototype.vi = function (t, i, n) {
          (t.yt = !1), (i.yt = !1);
          var s = this.Wt;
          if (s.yt()) {
            var h = s.R(),
              r = h.lastValueVisible,
              e = "" !== s.ar(),
              u = 0 === h.seriesLastValueMode,
              a = s.jh(!1);
            if (!a.qh) {
              r && ((t.Gt = this.lr(a, r, u)), (t.yt = 0 !== t.Gt.length)),
                (e || u) &&
                  ((i.Gt = this.cr(a, r, e, u)), (i.yt = i.Gt.length > 0));
              var o = s.ur(a.A),
                l = w(o);
              (n.t = l.t),
                (n.A = l.i),
                (n.ti = a.ti),
                (i.Tt = s.jt().Dt(a.ti / s.Ct().Yt())),
                (t.Tt = o);
            }
          }
        }),
        (i.prototype.cr = function (t, i, n, s) {
          var h = "",
            r = this.Wt.ar();
          return (
            n && 0 !== r.length && (h += "".concat(r, " ")),
            i && s && (h += this.Wt.Ct().vr() ? t._r : t.dr),
            h.trim()
          );
        }),
        (i.prototype.lr = function (t, i, n) {
          return i ? (n ? (this.Wt.Ct().vr() ? t.dr : t._r) : t.Gt) : "";
        }),
        i
      );
    })($),
    li = (function () {
      function t(t, i) {
        (this.wr = t), (this.Mr = i);
      }
      return (
        (t.prototype.br = function (t) {
          return null !== t && this.wr === t.wr && this.Mr === t.Mr;
        }),
        (t.prototype.mr = function () {
          return new t(this.wr, this.Mr);
        }),
        (t.prototype.gr = function () {
          return this.wr;
        }),
        (t.prototype.pr = function () {
          return this.Mr;
        }),
        (t.prototype.yr = function () {
          return this.Mr - this.wr;
        }),
        (t.prototype.wi = function () {
          return (
            this.Mr === this.wr ||
            Number.isNaN(this.Mr) ||
            Number.isNaN(this.wr)
          );
        }),
        (t.prototype.xn = function (i) {
          return null === i
            ? this
            : new t(Math.min(this.gr(), i.gr()), Math.max(this.pr(), i.pr()));
        }),
        (t.prototype.kr = function (t) {
          if (k(t) && 0 !== this.Mr - this.wr) {
            var i = 0.5 * (this.Mr + this.wr),
              n = this.Mr - i,
              s = this.wr - i;
            (n *= t), (s *= t), (this.Mr = i + n), (this.wr = i + s);
          }
        }),
        (t.prototype.Nr = function (t) {
          k(t) && ((this.Mr += t), (this.wr += t));
        }),
        (t.prototype.Cr = function () {
          return { minValue: this.wr, maxValue: this.Mr };
        }),
        (t.Sr = function (i) {
          return null === i ? null : new t(i.minValue, i.maxValue);
        }),
        t
      );
    })(),
    fi = (function () {
      function t(t, i) {
        (this.Tr = t), (this.Dr = i || null);
      }
      return (
        (t.prototype.Ar = function () {
          return this.Tr;
        }),
        (t.prototype.Br = function () {
          return this.Dr;
        }),
        (t.prototype.Cr = function () {
          return null === this.Tr
            ? null
            : { priceRange: this.Tr.Cr(), margins: this.Dr || void 0 };
        }),
        (t.Sr = function (i) {
          return null === i ? null : new t(li.Sr(i.priceRange), i.margins);
        }),
        t
      );
    })(),
    ci = (function (t) {
      function i(i, n) {
        var s = t.call(this, i) || this;
        return (s.Lr = n), s;
      }
      return (
        b(i, t),
        (i.prototype.bh = function (t, i) {
          var n = this.wh;
          n.yt = !1;
          var s = this.Lr.R();
          if (this.Kn.yt() && s.lineVisible) {
            var h = this.Lr.Er();
            null !== h &&
              ((n.yt = !0),
              (n.it = h),
              (n.A = s.color),
              (n.Ht = i),
              (n.Yt = t),
              (n.Vt = s.lineWidth),
              (n.Pt = s.lineStyle));
          }
        }),
        i
      );
    })(qt),
    vi = (function (t) {
      function i(i, n) {
        var s = t.call(this) || this;
        return (s.Vh = i), (s.Lr = n), s;
      }
      return (
        b(i, t),
        (i.prototype.vi = function (t, i, n) {
          (t.yt = !1), (i.yt = !1);
          var s = this.Lr.R(),
            h = s.axisLabelVisible,
            r = "" !== s.title,
            e = this.Vh;
          if (h && e.yt()) {
            var u = this.Lr.Er();
            if (null !== u) {
              r && ((i.Gt = s.title), (i.yt = !0)),
                (i.Tt = e.jt().Dt(u / e.Ct().Yt())),
                (t.Gt = e.Ct().Or(s.price)),
                (t.yt = !0);
              var a = w(s.color);
              (n.t = a.t), (n.A = a.i), (n.ti = u);
            }
          }
        }),
        i
      );
    })($),
    _i = (function () {
      function t(t, i) {
        (this.Vh = t),
          (this.zi = i),
          (this.Fr = new ci(t, this)),
          (this.uh = new vi(t, this)),
          (this.Vr = new It(this.uh, t, t.jt()));
      }
      return (
        (t.prototype.Pr = function (t) {
          y(this.zi, t), this.vt(), this.Vh.jt().Rr();
        }),
        (t.prototype.R = function () {
          return this.zi;
        }),
        (t.prototype.tn = function () {
          return [this.Fr, this.Vr];
        }),
        (t.prototype.zr = function () {
          return this.uh;
        }),
        (t.prototype.vt = function () {
          this.Fr.vt(), this.uh.vt();
        }),
        (t.prototype.Er = function () {
          var t = this.Vh,
            i = t.Ct();
          if (t.jt().bt().wi() || i.wi()) return null;
          var n = t.kt();
          return null === n ? null : i.Nt(this.zi.price, n.St);
        }),
        t
      );
    })(),
    di = (function (t) {
      function i(i) {
        var n = t.call(this) || this;
        return (n.gi = i), n;
      }
      return (
        b(i, t),
        (i.prototype.jt = function () {
          return this.gi;
        }),
        i
      );
    })(G),
    wi = { Ds: "", Hs: "", Us: "" },
    Mi = (function () {
      function t(t) {
        this.Vh = t;
      }
      return (
        (t.prototype.As = function (t, i) {
          var n = this.Vh.Wr(),
            s = this.Vh.R();
          switch (n) {
            case "Line":
              return this.Ir(s, t, i);
            case "Area":
              return this.jr(s);
            case "Baseline":
              return this.qr(s, t, i);
            case "Bar":
              return this.Ur(s, t, i);
            case "Candlestick":
              return this.Hr(s, t, i);
            case "Histogram":
              return this.Yr(s, t, i);
          }
          throw new Error("Unknown chart style");
        }),
        (t.prototype.Ur = function (t, i, n) {
          var s = m({}, wi),
            h = t.upColor,
            r = t.downColor,
            a = h,
            o = r,
            l = e(this.$r(i, n)),
            f = u(l.St[0]) <= u(l.St[3]);
          return (
            void 0 !== l.A
              ? ((s.Ds = l.A), (s.Hs = l.A))
              : ((s.Ds = f ? h : r), (s.Hs = f ? a : o)),
            s
          );
        }),
        (t.prototype.Hr = function (t, i, n) {
          var s,
            h,
            r,
            a = m({}, wi),
            o = t.upColor,
            l = t.downColor,
            f = t.borderUpColor,
            c = t.borderDownColor,
            v = t.wickUpColor,
            _ = t.wickDownColor,
            d = e(this.$r(i, n)),
            w = u(d.St[0]) <= u(d.St[3]);
          return (
            (a.Ds = null !== (s = d.A) && void 0 !== s ? s : w ? o : l),
            (a.Hs = null !== (h = d.Tt) && void 0 !== h ? h : w ? f : c),
            (a.Us = null !== (r = d.qs) && void 0 !== r ? r : w ? v : _),
            a
          );
        }),
        (t.prototype.jr = function (t) {
          return m(m({}, wi), { Ds: t.lineColor });
        }),
        (t.prototype.qr = function (t, i, n) {
          var s = e(this.$r(i, n)).St[3] >= t.baseValue.price;
          return m(m({}, wi), { Ds: s ? t.topLineColor : t.bottomLineColor });
        }),
        (t.prototype.Ir = function (t, i, n) {
          var s,
            h = e(this.$r(i, n));
          return m(m({}, wi), {
            Ds: null !== (s = h.A) && void 0 !== s ? s : t.color,
          });
        }),
        (t.prototype.Yr = function (t, i, n) {
          var s = m({}, wi),
            h = e(this.$r(i, n));
          return (s.Ds = void 0 !== h.A ? h.A : t.color), s;
        }),
        (t.prototype.$r = function (t, i) {
          return void 0 !== i ? i.St : this.Vh.an().Kr(t);
        }),
        t
      );
    })(),
    bi = 30,
    mi = (function () {
      function t() {
        (this.Xr = []), (this.Zr = new Map()), (this.Jr = new Map());
      }
      return (
        (t.prototype.Gr = function () {
          return this.hs() > 0 ? this.Xr[this.Xr.length - 1] : null;
        }),
        (t.prototype.Qr = function () {
          return this.hs() > 0 ? this.te(0) : null;
        }),
        (t.prototype.un = function () {
          return this.hs() > 0 ? this.te(this.Xr.length - 1) : null;
        }),
        (t.prototype.hs = function () {
          return this.Xr.length;
        }),
        (t.prototype.wi = function () {
          return 0 === this.hs();
        }),
        (t.prototype.Uh = function (t) {
          return null !== this.ie(t, 0);
        }),
        (t.prototype.Kr = function (t) {
          return this.ne(t);
        }),
        (t.prototype.ne = function (t, i) {
          void 0 === i && (i = 0);
          var n = this.ie(t, i);
          return null === n ? null : m(m({}, this.se(n)), { vs: this.te(n) });
        }),
        (t.prototype.fs = function () {
          return this.Xr;
        }),
        (t.prototype.he = function (t, i, n) {
          if (this.wi()) return null;
          for (var s = null, h = 0, r = n; h < r.length; h++) {
            var e = r[h];
            s = gi(s, this.re(t, i, e));
          }
          return s;
        }),
        (t.prototype.Z = function (t) {
          this.Jr.clear(), this.Zr.clear(), (this.Xr = t);
        }),
        (t.prototype.te = function (t) {
          return this.Xr[t].vs;
        }),
        (t.prototype.se = function (t) {
          return this.Xr[t];
        }),
        (t.prototype.ie = function (t, i) {
          var n = this.ee(t);
          if (null === n && 0 !== i)
            switch (i) {
              case -1:
                return this.ue(t);
              case 1:
                return this.ae(t);
              default:
                throw new TypeError("Unknown search mode");
            }
          return n;
        }),
        (t.prototype.ue = function (t) {
          var i = this.oe(t);
          return (
            i > 0 && (i -= 1), i !== this.Xr.length && this.te(i) < t ? i : null
          );
        }),
        (t.prototype.ae = function (t) {
          var i = this.le(t);
          return i !== this.Xr.length && t < this.te(i) ? i : null;
        }),
        (t.prototype.ee = function (t) {
          var i = this.oe(t);
          return i === this.Xr.length || t < this.Xr[i].vs ? null : i;
        }),
        (t.prototype.oe = function (t) {
          return ct(this.Xr, t, function (t, i) {
            return t.vs < i;
          });
        }),
        (t.prototype.le = function (t) {
          return vt(this.Xr, t, function (t, i) {
            return i.vs > t;
          });
        }),
        (t.prototype.fe = function (t, i, n) {
          for (var s = null, h = t; h < i; h++) {
            var r = this.Xr[h].St[n];
            Number.isNaN(r) ||
              (null === s
                ? (s = { ce: r, ve: r })
                : (r < s.ce && (s.ce = r), r > s.ve && (s.ve = r)));
          }
          return s;
        }),
        (t.prototype.re = function (t, i, n) {
          if (this.wi()) return null;
          var s = null,
            h = e(this.Qr()),
            r = e(this.un()),
            u = Math.max(t, h),
            a = Math.min(i, r),
            o = Math.ceil(u / bi) * bi,
            l = Math.max(o, Math.floor(a / bi) * bi),
            f = this.oe(u),
            c = this.le(Math.min(a, o, i));
          s = gi(s, this.fe(f, c, n));
          var v = this.Zr.get(n);
          void 0 === v && ((v = new Map()), this.Zr.set(n, v));
          for (var _ = Math.max(o + 1, u); _ < l; _ += bi) {
            var d = Math.floor(_ / bi),
              w = v.get(d);
            if (void 0 === w) {
              var M = this.oe(d * bi),
                b = this.le((d + 1) * bi - 1);
              (w = this.fe(M, b, n)), v.set(d, w);
            }
            s = gi(s, w);
          }
          (f = this.oe(l)), (c = this.le(a));
          return (s = gi(s, this.fe(f, c, n)));
        }),
        t
      );
    })();
  function gi(t, i) {
    return null === t
      ? i
      : null === i
      ? t
      : { ce: Math.min(t.ce, i.ce), ve: Math.max(t.ve, i.ve) };
  }
  var pi = (function (t) {
      function i(i, n, s) {
        var h = t.call(this, i) || this;
        (h.Bt = new mi()),
          (h.Fr = new ai(h)),
          (h._e = []),
          (h.de = new Ut(h)),
          (h.we = null),
          (h.Me = null),
          (h.be = []),
          (h.me = []),
          (h.ge = null),
          (h.zi = n),
          (h.pe = s);
        var r = new oi(h);
        return (
          (h.Ei = [r]),
          (h.Vr = new It(r, h, i)),
          ("Area" !== s && "Line" !== s && "Baseline" !== s) ||
            (h.we = new Xt(h)),
          h.ye(),
          h.ke(),
          h
        );
      }
      return (
        b(i, t),
        (i.prototype.p = function () {
          null !== this.ge && clearTimeout(this.ge);
        }),
        (i.prototype.ur = function (t) {
          return this.zi.priceLineColor || t;
        }),
        (i.prototype.jh = function (t) {
          var i = { qh: !0 },
            n = this.Ct();
          if (this.jt().bt().wi() || n.wi() || this.Bt.wi()) return i;
          var s,
            h,
            r = this.jt().bt().ss(),
            e = this.kt();
          if (null === r || null === e) return i;
          if (t) {
            var u = this.Bt.Gr();
            if (null === u) return i;
            (s = u), (h = u.vs);
          } else {
            var a = this.Bt.ne(r.jn(), -1);
            if (null === a) return i;
            if (null === (s = this.Bt.Kr(a.vs))) return i;
            h = a.vs;
          }
          var o = s.St[3],
            l = this.ls().As(h, { St: s }),
            f = n.Nt(o, e.St);
          return {
            qh: !1,
            et: o,
            Gt: n.Mi(o, e.St),
            _r: n.Or(o),
            dr: n.xe(o, e.St),
            A: l.Ds,
            ti: f,
            vs: h,
          };
        }),
        (i.prototype.ls = function () {
          return null !== this.Me || (this.Me = new Mi(this)), this.Me;
        }),
        (i.prototype.R = function () {
          return this.zi;
        }),
        (i.prototype.Pr = function (t) {
          var i = t.priceScaleId;
          void 0 !== i && i !== this.zi.priceScaleId && this.jt().Ne(this, i),
            y(this.zi, t),
            null !== this.ki &&
              void 0 !== t.scaleMargins &&
              this.ki.Pr({ scaleMargins: t.scaleMargins }),
            void 0 !== t.priceFormat && (this.ye(), this.jt().Ce()),
            this.jt().Se(this),
            this.jt().Te(),
            this.Hi.vt("options");
        }),
        (i.prototype.Z = function (t, i) {
          this.Bt.Z(t),
            this.De(),
            this.Hi.vt("data"),
            this.Wi.vt("data"),
            null !== this.we &&
              (i && i.Ae ? this.we.Rh() : 0 === t.length && this.we.Ph());
          var n = this.jt().oh(this);
          this.jt().Be(n), this.jt().Se(this), this.jt().Te(), this.jt().Rr();
        }),
        (i.prototype.Le = function (t) {
          (this.be = t.map(function (t) {
            return m({}, t);
          })),
            this.De();
          var i = this.jt().oh(this);
          this.Wi.vt("data"),
            this.jt().Be(i),
            this.jt().Se(this),
            this.jt().Te(),
            this.jt().Rr();
        }),
        (i.prototype.rr = function () {
          return this.me;
        }),
        (i.prototype.Ee = function (t) {
          var i = new _i(this, t);
          return this._e.push(i), this.jt().Se(this), i;
        }),
        (i.prototype.Oe = function (t) {
          var i = this._e.indexOf(t);
          -1 !== i && this._e.splice(i, 1), this.jt().Se(this);
        }),
        (i.prototype.Wr = function () {
          return this.pe;
        }),
        (i.prototype.kt = function () {
          var t = this.Fe();
          return null === t ? null : { St: t.St[3], Ve: t.rt };
        }),
        (i.prototype.Fe = function () {
          var t = this.jt().bt().ss();
          if (null === t) return null;
          var i = t.In();
          return this.Bt.ne(i, 1);
        }),
        (i.prototype.an = function () {
          return this.Bt;
        }),
        (i.prototype.er = function (t) {
          var i = this.Bt.Kr(t);
          return null === i
            ? null
            : "Bar" === this.pe || "Candlestick" === this.pe
            ? { open: i.St[0], high: i.St[1], low: i.St[2], close: i.St[3] }
            : i.St[3];
        }),
        (i.prototype.Pe = function (t) {
          var i = this,
            n = this.we;
          return null !== n && n.yt()
            ? (null === this.ge &&
                n.Wh() &&
                (this.ge = setTimeout(function () {
                  (i.ge = null), i.jt().Re();
                }, 0)),
              n.zh(),
              [n])
            : [];
        }),
        (i.prototype.tn = function () {
          var t = [];
          this.ze() || t.push(this.de);
          for (var i = 0, n = this._e; i < n.length; i++) {
            var s = n[i];
            t.push.apply(t, s.tn());
          }
          return t.push(this.Hi, this.Fr, this.Vr, this.Wi), t;
        }),
        (i.prototype.nn = function (t, i) {
          if (i !== this.ki && !this.ze()) return [];
          for (
            var n = g([], this.Ei, !0), s = 0, h = this._e;
            s < h.length;
            s++
          ) {
            var r = h[s];
            n.push(r.zr());
          }
          return n;
        }),
        (i.prototype.We = function (t, i) {
          var n = this;
          if (void 0 !== this.zi.autoscaleInfoProvider) {
            var s = this.zi.autoscaleInfoProvider(function () {
              var s = n.Ie(t, i);
              return null === s ? null : s.Cr();
            });
            return fi.Sr(s);
          }
          return this.Ie(t, i);
        }),
        (i.prototype.je = function () {
          return this.zi.priceFormat.minMove;
        }),
        (i.prototype.qe = function () {
          return this.Ue;
        }),
        (i.prototype.hn = function () {
          var t;
          this.Hi.vt(), this.Wi.vt();
          for (var i = 0, n = this.Ei; i < n.length; i++) {
            n[i].vt();
          }
          for (var s = 0, h = this._e; s < h.length; s++) {
            h[s].vt();
          }
          this.Fr.vt(),
            this.de.vt(),
            null === (t = this.we) || void 0 === t || t.vt();
        }),
        (i.prototype.Ct = function () {
          return e(t.prototype.Ct.call(this));
        }),
        (i.prototype.gt = function (t) {
          if (
            !(
              ("Line" === this.pe ||
                "Area" === this.pe ||
                "Baseline" === this.pe) &&
              this.zi.crosshairMarkerVisible
            )
          )
            return null;
          var i = this.Bt.Kr(t);
          return null === i
            ? null
            : { et: i.St[3], st: this.He(), Tt: this.Ye(), xt: this.$e(t) };
        }),
        (i.prototype.ar = function () {
          return this.zi.title;
        }),
        (i.prototype.yt = function () {
          return this.zi.visible;
        }),
        (i.prototype.ze = function () {
          return !tt(this.Ct().Ke());
        }),
        (i.prototype.Ie = function (t, i) {
          if (!x(t) || !x(i) || this.Bt.wi()) return null;
          var n =
              "Line" === this.pe ||
              "Area" === this.pe ||
              "Baseline" === this.pe ||
              "Histogram" === this.pe
                ? [3]
                : [2, 1],
            s = this.Bt.he(t, i, n),
            h = null !== s ? new li(s.ce, s.ve) : null;
          if ("Histogram" === this.Wr()) {
            var r = this.zi.base,
              e = new li(r, r);
            h = null !== h ? h.xn(e) : e;
          }
          return new fi(h, this.Wi.hr());
        }),
        (i.prototype.He = function () {
          switch (this.pe) {
            case "Line":
            case "Area":
            case "Baseline":
              return this.zi.crosshairMarkerRadius;
          }
          return 0;
        }),
        (i.prototype.Ye = function () {
          switch (this.pe) {
            case "Line":
            case "Area":
            case "Baseline":
              var t = this.zi.crosshairMarkerBorderColor;
              if (0 !== t.length) return t;
          }
          return null;
        }),
        (i.prototype.$e = function (t) {
          switch (this.pe) {
            case "Line":
            case "Area":
            case "Baseline":
              var i = this.zi.crosshairMarkerBackgroundColor;
              if (0 !== i.length) return i;
          }
          return this.ls().As(t).Ds;
        }),
        (i.prototype.ye = function () {
          switch (this.zi.priceFormat.type) {
            case "custom":
              this.Ue = { format: this.zi.priceFormat.formatter };
              break;
            case "volume":
              this.Ue = new et(this.zi.priceFormat.precision);
              break;
            case "percent":
              this.Ue = new rt(this.zi.priceFormat.precision);
              break;
            default:
              var t = Math.pow(10, this.zi.priceFormat.precision);
              this.Ue = new ht(t, this.zi.priceFormat.minMove * t);
          }
          null !== this.ki && this.ki.Xe();
        }),
        (i.prototype.De = function () {
          var t = this,
            i = this.jt().bt();
          if (i.wi() || 0 === this.Bt.hs()) this.me = [];
          else {
            var n = e(this.Bt.Qr());
            this.me = this.be.map(function (s, h) {
              var r = e(i.Ze(s.time, !0)),
                u = r < n ? 1 : -1;
              return {
                time: e(t.Bt.ne(r, u)).vs,
                position: s.position,
                shape: s.shape,
                color: s.color,
                id: s.id,
                Xh: h,
                text: s.text,
                size: s.size,
              };
            });
          }
        }),
        (i.prototype.ke = function () {
          switch (((this.Wi = new ui(this, this.jt())), this.pe)) {
            case "Bar":
              this.Hi = new yt(this, this.jt());
              break;
            case "Candlestick":
              this.Hi = new Lt(this, this.jt());
              break;
            case "Line":
              this.Hi = new Pt(this, this.jt());
              break;
            case "Area":
              this.Hi = new mt(this, this.jt());
              break;
            case "Baseline":
              this.Hi = new At(this, this.jt());
              break;
            case "Histogram":
              this.Hi = new Vt(this, this.jt());
              break;
            default:
              throw Error("Unknown chart style assigned: " + this.pe);
          }
        }),
        i
      );
    })(di),
    yi = (function () {
      function t(t) {
        this.zi = t;
      }
      return (
        (t.prototype.Je = function (t, i, n) {
          var s = t;
          if (0 === this.zi.mode) return s;
          var h = n.ji(),
            r = h.kt();
          if (null === r) return s;
          var e = h.Nt(t, r),
            a = n
              .Ge()
              .filter(function (t) {
                return t instanceof pi;
              })
              .reduce(function (t, s) {
                if (n.lh(s) || !s.yt()) return t;
                var h = s.Ct(),
                  r = s.an();
                if (h.wi() || !r.Uh(i)) return t;
                var e = r.Kr(i);
                if (null === e) return t;
                var a = u(s.kt());
                return t.concat([h.Nt(e.St[3], a.St)]);
              }, []);
          if (0 === a.length) return s;
          a.sort(function (t, i) {
            return Math.abs(t - e) - Math.abs(i - e);
          });
          var o = a[0];
          return (s = h.qi(o, r));
        }),
        t
      );
    })(),
    ki = (function () {
      function t() {
        this.Bt = null;
      }
      return (
        (t.prototype.Z = function (t) {
          this.Bt = t;
        }),
        (t.prototype.H = function (t, i, s, h) {
          var r = this;
          if (null !== this.Bt) {
            var u = Math.max(1, Math.floor(i));
            t.lineWidth = u;
            var a = Math.ceil(this.Bt.Ft * i),
              o = Math.ceil(this.Bt.Ot * i);
            !(function (t, i) {
              t.save(),
                t.lineWidth % 2 && t.translate(0.5, 0.5),
                i(),
                t.restore();
            })(t, function () {
              var s = e(r.Bt);
              if (s.Qe) {
                (t.strokeStyle = s.tu), n(t, s.iu), t.beginPath();
                for (var h = 0, l = s.nu; h < l.length; h++) {
                  var f = l[h],
                    c = Math.round(f.su * i);
                  t.moveTo(c, -u), t.lineTo(c, a + u);
                }
                t.stroke();
              }
              if (s.hu) {
                (t.strokeStyle = s.ru), n(t, s.eu), t.beginPath();
                for (var v = 0, _ = s.uu; v < _.length; v++) {
                  var d = _[v],
                    w = Math.round(d.su * i);
                  t.moveTo(-u, w), t.lineTo(o + u, w);
                }
                t.stroke();
              }
            });
          }
        }),
        t
      );
    })(),
    xi = (function () {
      function t(t) {
        (this.zt = new ki()), (this.ft = !0), (this.Di = t);
      }
      return (
        (t.prototype.vt = function () {
          this.ft = !0;
        }),
        (t.prototype.dt = function (t, i) {
          if (this.ft) {
            var n = this.Di.jt().R().grid,
              s = {
                Ft: t,
                Ot: i,
                hu: n.horzLines.visible,
                Qe: n.vertLines.visible,
                ru: n.horzLines.color,
                tu: n.vertLines.color,
                eu: n.horzLines.style,
                iu: n.vertLines.style,
                uu: this.Di.ji().au(),
                nu: this.Di.jt().bt().au() || [],
              };
            this.zt.Z(s), (this.ft = !1);
          }
          return this.zt;
        }),
        t
      );
    })(),
    Ni = (function () {
      function t(t) {
        this.Hi = new xi(t);
      }
      return (
        (t.prototype.ou = function () {
          return this.Hi;
        }),
        t
      );
    })(),
    Ci = { lu: 4, fu: 1e-4 };
  function Si(t, i) {
    var n = (100 * (t - i)) / i;
    return i < 0 ? -n : n;
  }
  function Ti(t, i) {
    var n = Si(t.gr(), i),
      s = Si(t.pr(), i);
    return new li(n, s);
  }
  function Di(t, i) {
    var n = (100 * (t - i)) / i + 100;
    return i < 0 ? -n : n;
  }
  function Ai(t, i) {
    var n = Di(t.gr(), i),
      s = Di(t.pr(), i);
    return new li(n, s);
  }
  function Bi(t, i) {
    var n = Math.abs(t);
    if (n < 1e-15) return 0;
    var s = Nt(n + i.fu) + i.lu;
    return t < 0 ? -s : s;
  }
  function Li(t, i) {
    var n = Math.abs(t);
    if (n < 1e-15) return 0;
    var s = Math.pow(10, n - i.lu) - i.fu;
    return t < 0 ? -s : s;
  }
  function Ei(t, i) {
    if (null === t) return null;
    var n = Bi(t.gr(), i),
      s = Bi(t.pr(), i);
    return new li(n, s);
  }
  function Oi(t, i) {
    if (null === t) return null;
    var n = Li(t.gr(), i),
      s = Li(t.pr(), i);
    return new li(n, s);
  }
  function Fi(t) {
    if (null === t) return Ci;
    var i = Math.abs(t.pr() - t.gr());
    if (i >= 1 || i < 1e-15) return Ci;
    var n = Math.ceil(Math.abs(Math.log10(i))),
      s = Ci.lu + n;
    return { lu: s, fu: 1 / Math.pow(10, s) };
  }
  var Vi,
    Pi = (function () {
      function t(t, i) {
        if (
          ((this.cu = t),
          (this.vu = i),
          (function (t) {
            if (t < 0) return !1;
            for (var i = t; i > 1; i /= 10) if (i % 10 != 0) return !1;
            return !0;
          })(this.cu))
        )
          this._u = [2, 2.5, 2];
        else {
          this._u = [];
          for (var n = this.cu; 1 !== n; ) {
            if (n % 2 == 0) this._u.push(2), (n /= 2);
            else {
              if (n % 5 != 0) throw new Error("unexpected base");
              this._u.push(2, 2.5), (n /= 5);
            }
            if (this._u.length > 100)
              throw new Error("something wrong with base");
          }
        }
      }
      return (
        (t.prototype.du = function (t, i, n) {
          for (
            var s,
              h,
              r,
              e = 0 === this.cu ? 0 : 1 / this.cu,
              u = Math.pow(10, Math.max(0, Math.ceil(Nt(t - i)))),
              a = 0,
              o = this.vu[0];
            ;

          ) {
            var l = xt(u, e, 1e-14) && u > e + 1e-14,
              f = xt(u, n * o, 1e-14),
              c = xt(u, 1, 1e-14);
            if (!(l && f && c)) break;
            (u /= o), (o = this.vu[++a % this.vu.length]);
          }
          if (
            (u <= e + 1e-14 && (u = e),
            (u = Math.max(1, u)),
            this._u.length > 0 &&
              ((s = u), (h = 1), (r = 1e-14), Math.abs(s - h) < r))
          )
            for (a = 0, o = this._u[0]; xt(u, n * o, 1e-14) && u > e + 1e-14; )
              (u /= o), (o = this._u[++a % this._u.length]);
          return u;
        }),
        t
      );
    })(),
    Ri = (function () {
      function t(t, i, n, s) {
        (this.wu = []),
          (this._i = t),
          (this.cu = i),
          (this.Mu = n),
          (this.bu = s);
      }
      return (
        (t.prototype.du = function (t, i) {
          if (t < i) throw new Error("high < low");
          var n = this._i.Yt(),
            s = ((t - i) * this.mu()) / n,
            h = new Pi(this.cu, [2, 2.5, 2]),
            r = new Pi(this.cu, [2, 2, 2.5]),
            e = new Pi(this.cu, [2.5, 2, 2]),
            u = [];
          return (
            u.push(h.du(t, i, s), r.du(t, i, s), e.du(t, i, s)),
            (function (t) {
              if (t.length < 1) throw Error("array is empty");
              for (var i = t[0], n = 1; n < t.length; ++n)
                t[n] < i && (i = t[n]);
              return i;
            })(u)
          );
        }),
        (t.prototype.gu = function () {
          var t = this._i,
            i = t.kt();
          if (null !== i) {
            var n = t.Yt(),
              s = this.Mu(n - 1, i),
              h = this.Mu(0, i),
              r = this._i.R().entireTextOnly ? this.pu() / 2 : 0,
              e = r,
              u = n - 1 - r,
              a = Math.max(s, h),
              o = Math.min(s, h);
            if (a !== o) {
              for (
                var l = this.du(a, o),
                  f = a % l,
                  c = a >= o ? 1 : -1,
                  v = null,
                  _ = 0,
                  d = a - (f += f < 0 ? l : 0);
                d > o;
                d -= l
              ) {
                var w = this.bu(d, i, !0);
                (null !== v && Math.abs(w - v) < this.mu()) ||
                  w < e ||
                  w > u ||
                  (_ < this.wu.length
                    ? ((this.wu[_].su = w), (this.wu[_].yu = t.ku(d)))
                    : this.wu.push({ su: w, yu: t.ku(d) }),
                  _++,
                  (v = w),
                  t.xu() && (l = this.du(d * c, o)));
              }
              this.wu.length = _;
            } else this.wu = [];
          } else this.wu = [];
        }),
        (t.prototype.au = function () {
          return this.wu;
        }),
        (t.prototype.pu = function () {
          return this._i.S();
        }),
        (t.prototype.mu = function () {
          return Math.ceil(2.5 * this.pu());
        }),
        t
      );
    })();
  function zi(t) {
    return t.slice().sort(function (t, i) {
      return e(t.Ni()) - e(i.Ni());
    });
  }
  !(function (t) {
    (t[(t.Normal = 0)] = "Normal"),
      (t[(t.Logarithmic = 1)] = "Logarithmic"),
      (t[(t.Percentage = 2)] = "Percentage"),
      (t[(t.IndexedTo100 = 3)] = "IndexedTo100");
  })(Vi || (Vi = {}));
  var Wi = new rt(),
    Ii = new ht(100, 1),
    ji = (function () {
      function t(t, i, n, s) {
        (this.Nu = 0),
          (this.Cu = null),
          (this.Tr = null),
          (this.Su = null),
          (this.Tu = { Du: !1, Au: null }),
          (this.Bu = 0),
          (this.Lu = 0),
          (this.Eu = new p()),
          (this.Ou = new p()),
          (this.Fu = []),
          (this.Vu = null),
          (this.Pu = null),
          (this.Ru = null),
          (this.zu = null),
          (this.Ue = Ii),
          (this.Wu = Fi(null)),
          (this.Iu = t),
          (this.zi = i),
          (this.ju = n),
          (this.qu = s),
          (this.Uu = new Ri(this, 100, this.Hu.bind(this), this.Yu.bind(this)));
      }
      return (
        (t.prototype.Ke = function () {
          return this.Iu;
        }),
        (t.prototype.R = function () {
          return this.zi;
        }),
        (t.prototype.Pr = function (t) {
          if (
            (y(this.zi, t),
            this.Xe(),
            void 0 !== t.mode && this.$u({ mh: t.mode }),
            void 0 !== t.scaleMargins)
          ) {
            var i = r(t.scaleMargins.top),
              n = r(t.scaleMargins.bottom);
            if (i < 0 || i > 1)
              throw new Error(
                "Invalid top margin - expect value between 0 and 1, given=".concat(
                  i
                )
              );
            if (n < 0 || n > 1 || i + n > 1)
              throw new Error(
                "Invalid bottom margin - expect value between 0 and 1, given=".concat(
                  n
                )
              );
            if (i + n > 1)
              throw new Error(
                "Invalid margins - sum of margins must be less than 1, given=".concat(
                  i + n
                )
              );
            this.Ku(), (this.Pu = null);
          }
        }),
        (t.prototype.Xu = function () {
          return this.zi.autoScale;
        }),
        (t.prototype.xu = function () {
          return 1 === this.zi.mode;
        }),
        (t.prototype.vr = function () {
          return 2 === this.zi.mode;
        }),
        (t.prototype.Zu = function () {
          return 3 === this.zi.mode;
        }),
        (t.prototype.mh = function () {
          return {
            _n: this.zi.autoScale,
            Ju: this.zi.invertScale,
            mh: this.zi.mode,
          };
        }),
        (t.prototype.$u = function (t) {
          var i = this.mh(),
            n = null;
          void 0 !== t._n && (this.zi.autoScale = t._n),
            void 0 !== t.mh &&
              ((this.zi.mode = t.mh),
              (2 !== t.mh && 3 !== t.mh) || (this.zi.autoScale = !0),
              (this.Tu.Du = !1)),
            1 === i.mh &&
              t.mh !== i.mh &&
              (!(function (t, i) {
                if (null === t) return !1;
                var n = Li(t.gr(), i),
                  s = Li(t.pr(), i);
                return isFinite(n) && isFinite(s);
              })(this.Tr, this.Wu)
                ? (this.zi.autoScale = !0)
                : null !== (n = Oi(this.Tr, this.Wu)) && this.Gu(n)),
            1 === t.mh &&
              t.mh !== i.mh &&
              null !== (n = Ei(this.Tr, this.Wu)) &&
              this.Gu(n);
          var s = i.mh !== this.zi.mode;
          s && (2 === i.mh || this.vr()) && this.Xe(),
            s && (3 === i.mh || this.Zu()) && this.Xe(),
            void 0 !== t.Ju &&
              i.Ju !== t.Ju &&
              ((this.zi.invertScale = t.Ju), this.Qu()),
            this.Ou.m(i, this.mh());
        }),
        (t.prototype.ta = function () {
          return this.Ou;
        }),
        (t.prototype.S = function () {
          return this.ju.fontSize;
        }),
        (t.prototype.Yt = function () {
          return this.Nu;
        }),
        (t.prototype.ia = function (t) {
          this.Nu !== t && ((this.Nu = t), this.Ku(), (this.Pu = null));
        }),
        (t.prototype.na = function () {
          if (this.Cu) return this.Cu;
          var t = this.Yt() - this.sa() - this.ha();
          return (this.Cu = t), t;
        }),
        (t.prototype.Ar = function () {
          return this.ra(), this.Tr;
        }),
        (t.prototype.Gu = function (t, i) {
          var n = this.Tr;
          (i || (null === n && null !== t) || (null !== n && !n.br(t))) &&
            ((this.Pu = null), (this.Tr = t));
        }),
        (t.prototype.wi = function () {
          return this.ra(), 0 === this.Nu || !this.Tr || this.Tr.wi();
        }),
        (t.prototype.ea = function (t) {
          return this.Ju() ? t : this.Yt() - 1 - t;
        }),
        (t.prototype.Nt = function (t, i) {
          return (
            this.vr() ? (t = Si(t, i)) : this.Zu() && (t = Di(t, i)),
            this.Yu(t, i)
          );
        }),
        (t.prototype.us = function (t, i, n) {
          this.ra();
          for (
            var s = this.ha(),
              h = e(this.Ar()),
              r = h.gr(),
              u = h.pr(),
              a = this.na() - 1,
              o = this.Ju(),
              l = a / (u - r),
              f = void 0 === n ? 0 : n.from,
              c = void 0 === n ? t.length : n.to,
              v = this.ua(),
              _ = f;
            _ < c;
            _++
          ) {
            var d = t[_],
              w = d.et;
            if (!isNaN(w)) {
              var M = w;
              null !== v && (M = v(d.et, i));
              var b = s + l * (M - r),
                m = o ? b : this.Nu - 1 - b;
              d.it = m;
            }
          }
        }),
        (t.prototype.Ss = function (t, i, n) {
          this.ra();
          for (
            var s = this.ha(),
              h = e(this.Ar()),
              r = h.gr(),
              u = h.pr(),
              a = this.na() - 1,
              o = this.Ju(),
              l = a / (u - r),
              f = void 0 === n ? 0 : n.from,
              c = void 0 === n ? t.length : n.to,
              v = this.ua(),
              _ = f;
            _ < c;
            _++
          ) {
            var d = t[_],
              w = d.open,
              M = d.high,
              b = d.low,
              m = d.close;
            null !== v &&
              ((w = v(d.open, i)),
              (M = v(d.high, i)),
              (b = v(d.low, i)),
              (m = v(d.close, i)));
            var g = s + l * (w - r),
              p = o ? g : this.Nu - 1 - g;
            (d.Ns = p),
              (g = s + l * (M - r)),
              (p = o ? g : this.Nu - 1 - g),
              (d.ys = p),
              (g = s + l * (b - r)),
              (p = o ? g : this.Nu - 1 - g),
              (d.ks = p),
              (g = s + l * (m - r)),
              (p = o ? g : this.Nu - 1 - g),
              (d.Cs = p);
          }
        }),
        (t.prototype.qi = function (t, i) {
          var n = this.Hu(t, i);
          return this.aa(n, i);
        }),
        (t.prototype.aa = function (t, i) {
          var n = t;
          return (
            this.vr()
              ? (n = (function (t, i) {
                  return i < 0 && (t = -t), (t / 100) * i + i;
                })(n, i))
              : this.Zu() &&
                (n = (function (t, i) {
                  return (t -= 100), i < 0 && (t = -t), (t / 100) * i + i;
                })(n, i)),
            n
          );
        }),
        (t.prototype.Ge = function () {
          return this.Fu;
        }),
        (t.prototype.oa = function () {
          if (this.Vu) return this.Vu;
          for (var t = [], i = 0; i < this.Fu.length; i++) {
            var n = this.Fu[i];
            null === n.Ni() && n.Ci(i + 1), t.push(n);
          }
          return (t = zi(t)), (this.Vu = t), this.Vu;
        }),
        (t.prototype.la = function (t) {
          -1 === this.Fu.indexOf(t) && (this.Fu.push(t), this.Xe(), this.fa());
        }),
        (t.prototype.ca = function (t) {
          var i = this.Fu.indexOf(t);
          if (-1 === i) throw new Error("source is not attached to scale");
          this.Fu.splice(i, 1),
            0 === this.Fu.length && (this.$u({ _n: !0 }), this.Gu(null)),
            this.Xe(),
            this.fa();
        }),
        (t.prototype.kt = function () {
          for (var t = null, i = 0, n = this.Fu; i < n.length; i++) {
            var s = n[i].kt();
            null !== s && (null === t || s.Ve < t.Ve) && (t = s);
          }
          return null === t ? null : t.St;
        }),
        (t.prototype.Ju = function () {
          return this.zi.invertScale;
        }),
        (t.prototype.au = function () {
          var t = null === this.kt();
          if (null !== this.Pu && (t || this.Pu.va === t)) return this.Pu.au;
          this.Uu.gu();
          var i = this.Uu.au();
          return (this.Pu = { au: i, va: t }), this.Eu.m(), i;
        }),
        (t.prototype._a = function () {
          return this.Eu;
        }),
        (t.prototype.da = function (t) {
          this.vr() ||
            this.Zu() ||
            (null === this.Ru &&
              null === this.Su &&
              (this.wi() ||
                ((this.Ru = this.Nu - t), (this.Su = e(this.Ar()).mr()))));
        }),
        (t.prototype.wa = function (t) {
          if (!this.vr() && !this.Zu() && null !== this.Ru) {
            this.$u({ _n: !1 }), (t = this.Nu - t) < 0 && (t = 0);
            var i = (this.Ru + 0.2 * (this.Nu - 1)) / (t + 0.2 * (this.Nu - 1)),
              n = e(this.Su).mr();
            (i = Math.max(i, 0.1)), n.kr(i), this.Gu(n);
          }
        }),
        (t.prototype.Ma = function () {
          this.vr() || this.Zu() || ((this.Ru = null), (this.Su = null));
        }),
        (t.prototype.ba = function (t) {
          this.Xu() ||
            (null === this.zu &&
              null === this.Su &&
              (this.wi() || ((this.zu = t), (this.Su = e(this.Ar()).mr()))));
        }),
        (t.prototype.ma = function (t) {
          if (!this.Xu() && null !== this.zu) {
            var i = e(this.Ar()).yr() / (this.na() - 1),
              n = t - this.zu;
            this.Ju() && (n *= -1);
            var s = n * i,
              h = e(this.Su).mr();
            h.Nr(s), this.Gu(h, !0), (this.Pu = null);
          }
        }),
        (t.prototype.ga = function () {
          this.Xu() ||
            (null !== this.zu && ((this.zu = null), (this.Su = null)));
        }),
        (t.prototype.qe = function () {
          return this.Ue || this.Xe(), this.Ue;
        }),
        (t.prototype.Mi = function (t, i) {
          switch (this.zi.mode) {
            case 2:
              return this.qe().format(Si(t, i));
            case 3:
              return this.qe().format(Di(t, i));
            default:
              return this.pa(t);
          }
        }),
        (t.prototype.ku = function (t) {
          switch (this.zi.mode) {
            case 2:
            case 3:
              return this.qe().format(t);
            default:
              return this.pa(t);
          }
        }),
        (t.prototype.Or = function (t) {
          return this.pa(t, e(this.ya()).qe());
        }),
        (t.prototype.xe = function (t, i) {
          return (t = Si(t, i)), Wi.format(t);
        }),
        (t.prototype.ka = function () {
          return this.Fu;
        }),
        (t.prototype.xa = function (t) {
          this.Tu = { Au: t, Du: !1 };
        }),
        (t.prototype.hn = function () {
          this.Fu.forEach(function (t) {
            return t.hn();
          });
        }),
        (t.prototype.Xe = function () {
          this.Pu = null;
          var t = this.ya(),
            i = 100;
          null !== t && (i = Math.round(1 / t.je())),
            (this.Ue = Ii),
            this.vr()
              ? ((this.Ue = Wi), (i = 100))
              : this.Zu()
              ? ((this.Ue = new ht(100, 1)), (i = 100))
              : null !== t && (this.Ue = t.qe()),
            (this.Uu = new Ri(this, i, this.Hu.bind(this), this.Yu.bind(this))),
            this.Uu.gu();
        }),
        (t.prototype.fa = function () {
          this.Vu = null;
        }),
        (t.prototype.ya = function () {
          return this.Fu[0] || null;
        }),
        (t.prototype.sa = function () {
          return this.Ju()
            ? this.zi.scaleMargins.bottom * this.Yt() + this.Lu
            : this.zi.scaleMargins.top * this.Yt() + this.Bu;
        }),
        (t.prototype.ha = function () {
          return this.Ju()
            ? this.zi.scaleMargins.top * this.Yt() + this.Bu
            : this.zi.scaleMargins.bottom * this.Yt() + this.Lu;
        }),
        (t.prototype.ra = function () {
          this.Tu.Du || ((this.Tu.Du = !0), this.Na());
        }),
        (t.prototype.Ku = function () {
          this.Cu = null;
        }),
        (t.prototype.Yu = function (t, i) {
          if ((this.ra(), this.wi())) return 0;
          t = this.xu() && t ? Bi(t, this.Wu) : t;
          var n = e(this.Ar()),
            s = this.ha() + ((this.na() - 1) * (t - n.gr())) / n.yr();
          return this.ea(s);
        }),
        (t.prototype.Hu = function (t, i) {
          if ((this.ra(), this.wi())) return 0;
          var n = this.ea(t),
            s = e(this.Ar()),
            h = s.gr() + s.yr() * ((n - this.ha()) / (this.na() - 1));
          return this.xu() ? Li(h, this.Wu) : h;
        }),
        (t.prototype.Qu = function () {
          (this.Pu = null), this.Uu.gu();
        }),
        (t.prototype.Na = function () {
          var t = this.Tu.Au;
          if (null !== t) {
            for (
              var i, n, s = null, h = 0, r = 0, u = 0, a = this.ka();
              u < a.length;
              u++
            ) {
              var o = a[u];
              if (o.yt()) {
                var l = o.kt();
                if (null !== l) {
                  var f = o.We(t.In(), t.jn()),
                    c = f && f.Ar();
                  if (null !== c) {
                    switch (this.zi.mode) {
                      case 1:
                        c = Ei(c, this.Wu);
                        break;
                      case 2:
                        c = Ti(c, l.St);
                        break;
                      case 3:
                        c = Ai(c, l.St);
                    }
                    if (((s = null === s ? c : s.xn(e(c))), null !== f)) {
                      var v = f.Br();
                      null !== v &&
                        ((h = Math.max(h, v.above)),
                        (r = Math.max(h, v.below)));
                    }
                  }
                }
              }
            }
            if (
              ((h === this.Bu && r === this.Lu) ||
                ((this.Bu = h), (this.Lu = r), (this.Pu = null), this.Ku()),
              null !== s)
            ) {
              if (s.gr() === s.pr()) {
                var _ = this.ya(),
                  d = 5 * (null === _ || this.vr() || this.Zu() ? 1 : _.je());
                this.xu() && (s = Oi(s, this.Wu)),
                  (s = new li(s.gr() - d, s.pr() + d)),
                  this.xu() && (s = Ei(s, this.Wu));
              }
              if (this.xu()) {
                var w = Oi(s, this.Wu),
                  M = Fi(w);
                if (((i = M), (n = this.Wu), i.lu !== n.lu || i.fu !== n.fu)) {
                  var b = null !== this.Su ? Oi(this.Su, this.Wu) : null;
                  (this.Wu = M),
                    (s = Ei(w, M)),
                    null !== b && (this.Su = Ei(b, M));
                }
              }
              this.Gu(s);
            } else
              null === this.Tr &&
                (this.Gu(new li(-0.5, 0.5)), (this.Wu = Fi(null)));
            this.Tu.Du = !0;
          }
        }),
        (t.prototype.ua = function () {
          var t = this;
          return this.vr()
            ? Si
            : this.Zu()
            ? Di
            : this.xu()
            ? function (i) {
                return Bi(i, t.Wu);
              }
            : null;
        }),
        (t.prototype.pa = function (t, i) {
          return void 0 === this.qu.priceFormatter
            ? (void 0 === i && (i = this.qe()), i.format(t))
            : this.qu.priceFormatter(t);
        }),
        t
      );
    })(),
    qi = (function () {
      function t(t, i) {
        (this.Fu = []),
          (this.Ca = new Map()),
          (this.Nu = 0),
          (this.hh = 0),
          (this.Sa = 1e3),
          (this.Vu = null),
          (this.Ta = new p()),
          (this.Da = t),
          (this.gi = i),
          (this.Aa = new Ni(this));
        var n = i.R();
        (this.Ba = this.La("left", n.leftPriceScale)),
          (this.Ea = this.La("right", n.rightPriceScale)),
          this.Ba.ta().u(this.Oa.bind(this, this.Ba), this),
          this.Ea.ta().u(this.Oa.bind(this, this.Ba), this),
          this.Fa(n);
      }
      return (
        (t.prototype.Fa = function (t) {
          if (
            (t.leftPriceScale && this.Ba.Pr(t.leftPriceScale),
            t.rightPriceScale && this.Ea.Pr(t.rightPriceScale),
            t.localization && (this.Ba.Xe(), this.Ea.Xe()),
            t.overlayPriceScales)
          )
            for (
              var i = 0, n = Array.from(this.Ca.values());
              i < n.length;
              i++
            ) {
              var s = e(n[i][0].Ct());
              s.Pr(t.overlayPriceScales), t.localization && s.Xe();
            }
        }),
        (t.prototype.Va = function (t) {
          switch (t) {
            case "left":
              return this.Ba;
            case "right":
              return this.Ea;
          }
          return this.Ca.has(t) ? r(this.Ca.get(t))[0].Ct() : null;
        }),
        (t.prototype.p = function () {
          this.jt().Pa().M(this),
            this.Ba.ta().M(this),
            this.Ea.ta().M(this),
            this.Fu.forEach(function (t) {
              t.p && t.p();
            }),
            this.Ta.m();
        }),
        (t.prototype.Ra = function () {
          return this.Sa;
        }),
        (t.prototype.za = function (t) {
          this.Sa = t;
        }),
        (t.prototype.jt = function () {
          return this.gi;
        }),
        (t.prototype.Ht = function () {
          return this.hh;
        }),
        (t.prototype.Yt = function () {
          return this.Nu;
        }),
        (t.prototype.Wa = function (t) {
          (this.hh = t), this.Ia();
        }),
        (t.prototype.ia = function (t) {
          var i = this;
          (this.Nu = t),
            this.Ba.ia(t),
            this.Ea.ia(t),
            this.Fu.forEach(function (n) {
              if (i.lh(n)) {
                var s = n.Ct();
                null !== s && s.ia(t);
              }
            }),
            this.Ia();
        }),
        (t.prototype.Ge = function () {
          return this.Fu;
        }),
        (t.prototype.lh = function (t) {
          var i = t.Ct();
          return null === i || (this.Ba !== i && this.Ea !== i);
        }),
        (t.prototype.la = function (t, i, n) {
          var s = void 0 !== n ? n : this.qa().ja + 1;
          this.Ua(t, i, s);
        }),
        (t.prototype.ca = function (t) {
          var i = this.Fu.indexOf(t);
          h(-1 !== i, "removeDataSource: invalid data source"),
            this.Fu.splice(i, 1);
          var n = e(t.Ct()).Ke();
          if (this.Ca.has(n)) {
            var s = r(this.Ca.get(n)),
              u = s.indexOf(t);
            -1 !== u && (s.splice(u, 1), 0 === s.length && this.Ca.delete(n));
          }
          var a = t.Ct();
          a && a.Ge().indexOf(t) >= 0 && a.ca(t),
            null !== a && (a.fa(), this.Ha(a)),
            (this.Vu = null);
        }),
        (t.prototype._h = function (t) {
          return t === this.Ba ? "left" : t === this.Ea ? "right" : "overlay";
        }),
        (t.prototype.Ya = function () {
          return this.Ba;
        }),
        (t.prototype.$a = function () {
          return this.Ea;
        }),
        (t.prototype.Ka = function (t, i) {
          t.da(i);
        }),
        (t.prototype.Xa = function (t, i) {
          t.wa(i), this.Ia();
        }),
        (t.prototype.Za = function (t) {
          t.Ma();
        }),
        (t.prototype.Ja = function (t, i) {
          t.ba(i);
        }),
        (t.prototype.Ga = function (t, i) {
          t.ma(i), this.Ia();
        }),
        (t.prototype.Qa = function (t) {
          t.ga();
        }),
        (t.prototype.Ia = function () {
          this.Fu.forEach(function (t) {
            t.hn();
          });
        }),
        (t.prototype.ji = function () {
          var t = null;
          return (
            this.gi.R().rightPriceScale.visible && 0 !== this.Ea.Ge().length
              ? (t = this.Ea)
              : this.gi.R().leftPriceScale.visible && 0 !== this.Ba.Ge().length
              ? (t = this.Ba)
              : 0 !== this.Fu.length && (t = this.Fu[0].Ct()),
            null === t && (t = this.Ea),
            t
          );
        }),
        (t.prototype.fh = function () {
          var t = null;
          return (
            this.gi.R().rightPriceScale.visible
              ? (t = this.Ea)
              : this.gi.R().leftPriceScale.visible && (t = this.Ba),
            t
          );
        }),
        (t.prototype.Ha = function (t) {
          null !== t && t.Xu() && this.io(t);
        }),
        (t.prototype.no = function (t) {
          var i = this.Da.ss();
          t.$u({ _n: !0 }), null !== i && t.xa(i), this.Ia();
        }),
        (t.prototype.so = function () {
          this.io(this.Ba), this.io(this.Ea);
        }),
        (t.prototype.ho = function () {
          var t = this;
          this.Ha(this.Ba),
            this.Ha(this.Ea),
            this.Fu.forEach(function (i) {
              t.lh(i) && t.Ha(i.Ct());
            }),
            this.Ia(),
            this.gi.Rr();
        }),
        (t.prototype.oa = function () {
          return null === this.Vu && (this.Vu = zi(this.Fu)), this.Vu;
        }),
        (t.prototype.ro = function () {
          return this.Ta;
        }),
        (t.prototype.eo = function () {
          return this.Aa;
        }),
        (t.prototype.io = function (t) {
          var i = t.ka();
          if (i && i.length > 0 && !this.Da.wi()) {
            var n = this.Da.ss();
            null !== n && t.xa(n);
          }
          t.hn();
        }),
        (t.prototype.qa = function () {
          var t = this.oa();
          if (0 === t.length) return { uo: 0, ja: 0 };
          for (var i = 0, n = 0, s = 0; s < t.length; s++) {
            var h = t[s].Ni();
            null !== h && (h < i && (i = h), h > n && (n = h));
          }
          return { uo: i, ja: n };
        }),
        (t.prototype.Ua = function (t, i, n) {
          var s = this.Va(i);
          if (
            (null === s && (s = this.La(i, this.gi.R().overlayPriceScales)),
            this.Fu.push(t),
            !tt(i))
          ) {
            var h = this.Ca.get(i) || [];
            h.push(t), this.Ca.set(i, h);
          }
          s.la(t), t.Si(s), t.Ci(n), this.Ha(s), (this.Vu = null);
        }),
        (t.prototype.Oa = function (t, i, n) {
          i.mh !== n.mh && this.io(t);
        }),
        (t.prototype.La = function (t, i) {
          var n = m({ visible: !0, autoScale: !0 }, S(i)),
            s = new ji(t, n, this.gi.R().layout, this.gi.R().localization);
          return s.ia(this.Yt()), s;
        }),
        t
      );
    })(),
    Ui = function (t) {
      return t.getUTCFullYear();
    };
  function Hi(t, i, n) {
    return i
      .replace(
        /yyyy/g,
        (function (t) {
          return st(Ui(t), 4);
        })(t)
      )
      .replace(
        /yy/g,
        (function (t) {
          return st(Ui(t) % 100, 2);
        })(t)
      )
      .replace(
        /MMMM/g,
        (function (t, i) {
          return new Date(
            t.getUTCFullYear(),
            t.getUTCMonth(),
            1
          ).toLocaleString(i, { month: "long" });
        })(t, n)
      )
      .replace(
        /MMM/g,
        (function (t, i) {
          return new Date(
            t.getUTCFullYear(),
            t.getUTCMonth(),
            1
          ).toLocaleString(i, { month: "short" });
        })(t, n)
      )
      .replace(
        /MM/g,
        (function (t) {
          return st(
            (function (t) {
              return t.getUTCMonth() + 1;
            })(t),
            2
          );
        })(t)
      )
      .replace(
        /dd/g,
        (function (t) {
          return st(
            (function (t) {
              return t.getUTCDate();
            })(t),
            2
          );
        })(t)
      );
  }
  var Yi = (function () {
      function t(t, i) {
        void 0 === t && (t = "yyyy-MM-dd"),
          void 0 === i && (i = "default"),
          (this.ao = t),
          (this.oo = i);
      }
      return (
        (t.prototype.lo = function (t) {
          return Hi(t, this.ao, this.oo);
        }),
        t
      );
    })(),
    $i = (function () {
      function t(t) {
        this.fo = t || "%h:%m:%s";
      }
      return (
        (t.prototype.lo = function (t) {
          return this.fo
            .replace("%h", st(t.getUTCHours(), 2))
            .replace("%m", st(t.getUTCMinutes(), 2))
            .replace("%s", st(t.getUTCSeconds(), 2));
        }),
        t
      );
    })(),
    Ki = { co: "yyyy-MM-dd", vo: "%h:%m:%s", _o: " ", do: "default" },
    Xi = (function () {
      function t(t) {
        void 0 === t && (t = {});
        var i = m(m({}, Ki), t);
        (this.wo = new Yi(i.co, i.do)),
          (this.Mo = new $i(i.vo)),
          (this.bo = i._o);
      }
      return (
        (t.prototype.lo = function (t) {
          return "".concat(this.wo.lo(t)).concat(this.bo).concat(this.Mo.lo(t));
        }),
        t
      );
    })();
  var Zi = (function () {
      function t(t, i) {
        void 0 === i && (i = 50),
          (this.mo = 0),
          (this.po = 1),
          (this.yo = 1),
          (this.Gs = new Map()),
          (this.ko = new Map()),
          (this.xo = t),
          (this.No = i);
      }
      return (
        (t.prototype.lo = function (t) {
          var i =
              void 0 === t.Co
                ? new Date(1e3 * t.So).getTime()
                : new Date(
                    Date.UTC(t.Co.year, t.Co.month - 1, t.Co.day)
                  ).getTime(),
            n = this.Gs.get(i);
          if (void 0 !== n) return n.To;
          if (this.mo === this.No) {
            var s = this.ko.get(this.yo);
            this.ko.delete(this.yo), this.Gs.delete(r(s)), this.yo++, this.mo--;
          }
          var h = this.xo(t);
          return (
            this.Gs.set(i, { To: h, Do: this.po }),
            this.ko.set(this.po, i),
            this.mo++,
            this.po++,
            h
          );
        }),
        t
      );
    })(),
    Ji = (function () {
      function t(t, i) {
        h(t <= i, "right should be >= left"), (this.Ao = t), (this.Bo = i);
      }
      return (
        (t.prototype.In = function () {
          return this.Ao;
        }),
        (t.prototype.jn = function () {
          return this.Bo;
        }),
        (t.prototype.Lo = function () {
          return this.Bo - this.Ao + 1;
        }),
        (t.prototype.Uh = function (t) {
          return this.Ao <= t && t <= this.Bo;
        }),
        (t.prototype.br = function (t) {
          return this.Ao === t.In() && this.Bo === t.jn();
        }),
        t
      );
    })();
  function Gi(t, i) {
    return null === t || null === i ? t === i : t.br(i);
  }
  var Qi,
    tn = (function () {
      function t() {
        (this.Eo = new Map()), (this.Gs = null);
      }
      return (
        (t.prototype.Oo = function (t, i) {
          this.Fo(i), (this.Gs = null);
          for (var n = i; n < t.length; ++n) {
            var s = t[n],
              h = this.Eo.get(s.Vo);
            void 0 === h && ((h = []), this.Eo.set(s.Vo, h)),
              h.push({ vs: n, rt: s.rt, Po: s.Vo });
          }
        }),
        (t.prototype.Ro = function (t, i) {
          var n = Math.ceil(i / t);
          return (
            (null !== this.Gs && this.Gs.zo === n) ||
              (this.Gs = { au: this.Wo(n), zo: n }),
            this.Gs.au
          );
        }),
        (t.prototype.Fo = function (t) {
          if (0 !== t) {
            var i = [];
            this.Eo.forEach(function (n, s) {
              t <= n[0].vs
                ? i.push(s)
                : n.splice(
                    ct(n, t, function (i) {
                      return i.vs < t;
                    }),
                    1 / 0
                  );
            });
            for (var n = 0, s = i; n < s.length; n++) {
              var h = s[n];
              this.Eo.delete(h);
            }
          } else this.Eo.clear();
        }),
        (t.prototype.Wo = function (t) {
          for (
            var i = [],
              n = 0,
              s = Array.from(this.Eo.keys()).sort(function (t, i) {
                return i - t;
              });
            n < s.length;
            n++
          ) {
            var h = s[n];
            if (this.Eo.get(h)) {
              var e = i;
              i = [];
              for (
                var u = e.length,
                  a = 0,
                  o = r(this.Eo.get(h)),
                  l = o.length,
                  f = 1 / 0,
                  c = -1 / 0,
                  v = 0;
                v < l;
                v++
              ) {
                for (var _ = o[v], d = _.vs; a < u; ) {
                  var w = e[a],
                    M = w.vs;
                  if (!(M < d)) {
                    f = M;
                    break;
                  }
                  a++, i.push(w), (c = M), (f = 1 / 0);
                }
                f - d >= t && d - c >= t && (i.push(_), (c = d));
              }
              for (; a < u; a++) i.push(e[a]);
            }
          }
          return i;
        }),
        t
      );
    })(),
    nn = (function () {
      function t(t) {
        this.Io = t;
      }
      return (
        (t.prototype.jo = function () {
          return null === this.Io
            ? null
            : new Ji(Math.floor(this.Io.In()), Math.ceil(this.Io.jn()));
        }),
        (t.prototype.qo = function () {
          return this.Io;
        }),
        (t.Uo = function () {
          return new t(null);
        }),
        t
      );
    })();
  !(function (t) {
    (t[(t.Year = 0)] = "Year"),
      (t[(t.Month = 1)] = "Month"),
      (t[(t.DayOfMonth = 2)] = "DayOfMonth"),
      (t[(t.Time = 3)] = "Time"),
      (t[(t.TimeWithSeconds = 4)] = "TimeWithSeconds");
  })(Qi || (Qi = {}));
  var sn = (function () {
    function t(t, i, n) {
      (this.hh = 0),
        (this.Ho = null),
        (this.Yo = []),
        (this.zu = null),
        (this.Ru = null),
        (this.$o = new tn()),
        (this.Ko = new Map()),
        (this.Xo = nn.Uo()),
        (this.Zo = !0),
        (this.Jo = new p()),
        (this.Go = new p()),
        (this.Qo = new p()),
        (this.tl = null),
        (this.il = null),
        (this.nl = []),
        (this.zi = i),
        (this.qu = n),
        (this.sl = i.rightOffset),
        (this.hl = i.barSpacing),
        (this.gi = t),
        this.rl();
    }
    return (
      (t.prototype.R = function () {
        return this.zi;
      }),
      (t.prototype.el = function (t) {
        y(this.qu, t), this.ul(), this.rl();
      }),
      (t.prototype.Pr = function (t, i) {
        var n;
        y(this.zi, t),
          this.zi.fixLeftEdge && this.al(),
          this.zi.fixRightEdge && this.ol(),
          void 0 !== t.barSpacing && this.gi.pn(t.barSpacing),
          void 0 !== t.rightOffset && this.gi.yn(t.rightOffset),
          void 0 !== t.minBarSpacing &&
            this.gi.pn(
              null !== (n = t.barSpacing) && void 0 !== n ? n : this.hl
            ),
          this.ul(),
          this.rl(),
          this.Qo.m();
      }),
      (t.prototype.pi = function (t) {
        var i;
        return (
          (null === (i = this.Yo[t]) || void 0 === i ? void 0 : i.rt) || null
        );
      }),
      (t.prototype.Ze = function (t, i) {
        if (this.Yo.length < 1) return null;
        if (t.So > this.Yo[this.Yo.length - 1].rt.So)
          return i ? this.Yo.length - 1 : null;
        var n = ct(this.Yo, t.So, function (t, i) {
          return t.rt.So < i;
        });
        return t.So < this.Yo[n].rt.So ? (i ? n : null) : n;
      }),
      (t.prototype.wi = function () {
        return 0 === this.hh || 0 === this.Yo.length || null === this.Ho;
      }),
      (t.prototype.ss = function () {
        return this.ll(), this.Xo.jo();
      }),
      (t.prototype.fl = function () {
        return this.ll(), this.Xo.qo();
      }),
      (t.prototype.cl = function () {
        var t = this.ss();
        if (null === t) return null;
        var i = { from: t.In(), to: t.jn() };
        return this.vl(i);
      }),
      (t.prototype.vl = function (t) {
        var i = Math.round(t.from),
          n = Math.round(t.to),
          s = e(this._l()),
          h = e(this.dl());
        return {
          from: e(this.pi(Math.max(s, i))),
          to: e(this.pi(Math.min(h, n))),
        };
      }),
      (t.prototype.wl = function (t) {
        return { from: e(this.Ze(t.from, !0)), to: e(this.Ze(t.to, !0)) };
      }),
      (t.prototype.Ht = function () {
        return this.hh;
      }),
      (t.prototype.Wa = function (t) {
        if (isFinite(t) && !(t <= 0) && this.hh !== t) {
          if (this.zi.lockVisibleTimeRangeOnResize && this.hh) {
            var i = (this.hl * t) / this.hh;
            this.hl = i;
          }
          if (this.zi.fixLeftEdge) {
            var n = this.ss();
            if (null !== n)
              if (n.In() <= 0) {
                var s = this.hh - t;
                this.sl -= Math.round(s / this.hl) + 1;
              }
          }
          (this.hh = t), (this.Zo = !0), this.Ml(), this.bl();
        }
      }),
      (t.prototype.At = function (t) {
        if (this.wi() || !x(t)) return 0;
        var i = this.ml() + this.sl - t;
        return this.hh - (i + 0.5) * this.hl - 1;
      }),
      (t.prototype.es = function (t, i) {
        for (
          var n = this.ml(),
            s = void 0 === i ? 0 : i.from,
            h = void 0 === i ? t.length : i.to,
            r = s;
          r < h;
          r++
        ) {
          var e = t[r].rt,
            u = n + this.sl - e,
            a = this.hh - (u + 0.5) * this.hl - 1;
          t[r].tt = a;
        }
      }),
      (t.prototype.gl = function (t) {
        return Math.ceil(this.pl(t));
      }),
      (t.prototype.yn = function (t) {
        (this.Zo = !0), (this.sl = t), this.bl(), this.gi.yl(), this.gi.Rr();
      }),
      (t.prototype.ws = function () {
        return this.hl;
      }),
      (t.prototype.pn = function (t) {
        this.kl(t), this.bl(), this.gi.yl(), this.gi.Rr();
      }),
      (t.prototype.xl = function () {
        return this.sl;
      }),
      (t.prototype.au = function () {
        if (this.wi()) return null;
        if (null !== this.il) return this.il;
        for (
          var t = this.hl,
            i = 5 * (this.gi.R().layout.fontSize + 4),
            n = Math.round(i / t),
            s = e(this.ss()),
            h = Math.max(s.In(), s.In() - n),
            r = Math.max(s.jn(), s.jn() - n),
            u = this.$o.Ro(t, i),
            a = this._l() + n,
            o = this.dl() - n,
            l = this.Nl(),
            f = this.zi.fixLeftEdge || l,
            c = this.zi.fixRightEdge || l,
            v = 0,
            _ = 0,
            d = u;
          _ < d.length;
          _++
        ) {
          var w = d[_];
          if (h <= w.vs && w.vs <= r) {
            var M = void 0;
            v < this.nl.length
              ? (((M = this.nl[v]).su = this.At(w.vs)),
                (M.yu = this.Cl(w.rt, w.Po)),
                (M.Po = w.Po))
              : ((M = {
                  Sl: !1,
                  su: this.At(w.vs),
                  yu: this.Cl(w.rt, w.Po),
                  Po: w.Po,
                }),
                this.nl.push(M)),
              this.hl > i / 2 && !l
                ? (M.Sl = !1)
                : (M.Sl = (f && w.vs <= a) || (c && w.vs >= o)),
              v++;
          }
        }
        return (this.nl.length = v), (this.il = this.nl), this.nl;
      }),
      (t.prototype.Tl = function () {
        (this.Zo = !0),
          this.pn(this.zi.barSpacing),
          this.yn(this.zi.rightOffset);
      }),
      (t.prototype.Dl = function (t) {
        (this.Zo = !0), (this.Ho = t), this.bl(), this.al();
      }),
      (t.prototype.Al = function (t, i) {
        var n = this.pl(t),
          s = this.ws(),
          h = s + i * (s / 10);
        this.pn(h),
          this.zi.rightBarStaysOnScroll ||
            this.yn(this.xl() + (n - this.pl(t)));
      }),
      (t.prototype.da = function (t) {
        this.zu && this.ga(),
          null === this.Ru &&
            null === this.tl &&
            (this.wi() || ((this.Ru = t), this.Bl()));
      }),
      (t.prototype.wa = function (t) {
        if (null !== this.tl) {
          var i = kt(this.hh - t, 0, this.hh),
            n = kt(this.hh - e(this.Ru), 0, this.hh);
          0 !== i && 0 !== n && this.pn((this.tl.ws * i) / n);
        }
      }),
      (t.prototype.Ma = function () {
        null !== this.Ru && ((this.Ru = null), this.Ll());
      }),
      (t.prototype.ba = function (t) {
        null === this.zu &&
          null === this.tl &&
          (this.wi() || ((this.zu = t), this.Bl()));
      }),
      (t.prototype.ma = function (t) {
        if (null !== this.zu) {
          var i = (this.zu - t) / this.ws();
          (this.sl = e(this.tl).xl + i), (this.Zo = !0), this.bl();
        }
      }),
      (t.prototype.ga = function () {
        null !== this.zu && ((this.zu = null), this.Ll());
      }),
      (t.prototype.El = function () {
        this.Ol(this.zi.rightOffset);
      }),
      (t.prototype.Ol = function (t, i) {
        var n = this;
        if ((void 0 === i && (i = 400), !isFinite(t)))
          throw new RangeError("offset is required and must be finite number");
        if (!isFinite(i) || i <= 0)
          throw new RangeError(
            "animationDuration (optional) must be finite positive number"
          );
        var s = this.sl,
          h = performance.now(),
          r = function () {
            var e = (performance.now() - h) / i,
              u = e >= 1,
              a = u ? t : s + (t - s) * e;
            n.yn(a), u || setTimeout(r, 20);
          };
        r();
      }),
      (t.prototype.vt = function (t, i) {
        (this.Zo = !0), (this.Yo = t), this.$o.Oo(t, i), this.bl();
      }),
      (t.prototype.Fl = function () {
        return this.Jo;
      }),
      (t.prototype.Vl = function () {
        return this.Go;
      }),
      (t.prototype.Pl = function () {
        return this.Qo;
      }),
      (t.prototype.ml = function () {
        return this.Ho || 0;
      }),
      (t.prototype.Rl = function (t) {
        var i = t.Lo();
        this.kl(this.hh / i),
          (this.sl = t.jn() - this.ml()),
          this.bl(),
          (this.Zo = !0),
          this.gi.yl(),
          this.gi.Rr();
      }),
      (t.prototype.zl = function () {
        var t = this._l(),
          i = this.dl();
        null !== t && null !== i && this.Rl(new Ji(t, i + this.zi.rightOffset));
      }),
      (t.prototype.Wl = function (t) {
        var i = new Ji(t.from, t.to);
        this.Rl(i);
      }),
      (t.prototype.yi = function (t) {
        return void 0 !== this.qu.timeFormatter
          ? this.qu.timeFormatter(t.Co || t.So)
          : this.Il.lo(new Date(1e3 * t.So));
      }),
      (t.prototype.Nl = function () {
        var t = this.gi.R(),
          i = t.handleScroll,
          n = t.handleScale;
        return !(
          i.horzTouchDrag ||
          i.mouseWheel ||
          i.pressedMouseMove ||
          i.vertTouchDrag ||
          n.axisDoubleClickReset ||
          n.axisPressedMouseMove.time ||
          n.mouseWheel ||
          n.pinch
        );
      }),
      (t.prototype._l = function () {
        return 0 === this.Yo.length ? null : 0;
      }),
      (t.prototype.dl = function () {
        return 0 === this.Yo.length ? null : this.Yo.length - 1;
      }),
      (t.prototype.jl = function (t) {
        return (this.hh - 1 - t) / this.hl;
      }),
      (t.prototype.pl = function (t) {
        var i = this.jl(t),
          n = this.ml() + this.sl - i;
        return Math.round(1e6 * n) / 1e6;
      }),
      (t.prototype.kl = function (t) {
        var i = this.hl;
        (this.hl = t), this.Ml(), i !== this.hl && ((this.Zo = !0), this.ql());
      }),
      (t.prototype.ll = function () {
        if (this.Zo)
          if (((this.Zo = !1), this.wi())) this.Ul(nn.Uo());
          else {
            var t = this.ml(),
              i = this.hh / this.hl,
              n = this.sl + t,
              s = new Ji(n - i + 1, n);
            this.Ul(new nn(s));
          }
      }),
      (t.prototype.Ml = function () {
        var t = this.Hl();
        if ((this.hl < t && ((this.hl = t), (this.Zo = !0)), 0 !== this.hh)) {
          var i = 0.5 * this.hh;
          this.hl > i && ((this.hl = i), (this.Zo = !0));
        }
      }),
      (t.prototype.Hl = function () {
        return this.zi.fixLeftEdge &&
          this.zi.fixRightEdge &&
          0 !== this.Yo.length
          ? this.hh / this.Yo.length
          : this.zi.minBarSpacing;
      }),
      (t.prototype.bl = function () {
        var t = this.Yl();
        this.sl > t && ((this.sl = t), (this.Zo = !0));
        var i = this.$l();
        null !== i && this.sl < i && ((this.sl = i), (this.Zo = !0));
      }),
      (t.prototype.$l = function () {
        var t = this._l(),
          i = this.Ho;
        return null === t || null === i
          ? null
          : t -
              i -
              1 +
              (this.zi.fixLeftEdge
                ? this.hh / this.hl
                : Math.min(2, this.Yo.length));
      }),
      (t.prototype.Yl = function () {
        return this.zi.fixRightEdge
          ? 0
          : this.hh / this.hl - Math.min(2, this.Yo.length);
      }),
      (t.prototype.Bl = function () {
        this.tl = { ws: this.ws(), xl: this.xl() };
      }),
      (t.prototype.Ll = function () {
        this.tl = null;
      }),
      (t.prototype.Cl = function (t, i) {
        var n = this,
          s = this.Ko.get(i);
        return (
          void 0 === s &&
            ((s = new Zi(function (t) {
              return n.Kl(t, i);
            })),
            this.Ko.set(i, s)),
          s.lo(t)
        );
      }),
      (t.prototype.Kl = function (t, i) {
        var n,
          s = (function (t, i, n) {
            switch (t) {
              case 0:
              case 10:
                return i ? (n ? 4 : 3) : 2;
              case 20:
              case 21:
              case 22:
              case 30:
              case 31:
              case 32:
              case 33:
                return i ? 3 : 2;
              case 50:
                return 2;
              case 60:
                return 1;
              case 70:
                return 0;
            }
          })(i, this.zi.timeVisible, this.zi.secondsVisible);
        return void 0 !== this.zi.tickMarkFormatter
          ? this.zi.tickMarkFormatter(
              null !== (n = t.Co) && void 0 !== n ? n : t.So,
              s,
              this.qu.locale
            )
          : (function (t, i, n) {
              var s = {};
              switch (i) {
                case 0:
                  s.year = "numeric";
                  break;
                case 1:
                  s.month = "short";
                  break;
                case 2:
                  s.day = "numeric";
                  break;
                case 3:
                  (s.hour12 = !1), (s.hour = "2-digit"), (s.minute = "2-digit");
                  break;
                case 4:
                  (s.hour12 = !1),
                    (s.hour = "2-digit"),
                    (s.minute = "2-digit"),
                    (s.second = "2-digit");
              }
              var h =
                void 0 === t.Co
                  ? new Date(1e3 * t.So)
                  : new Date(Date.UTC(t.Co.year, t.Co.month - 1, t.Co.day));
              return new Date(
                h.getUTCFullYear(),
                h.getUTCMonth(),
                h.getUTCDate(),
                h.getUTCHours(),
                h.getUTCMinutes(),
                h.getUTCSeconds(),
                h.getUTCMilliseconds()
              ).toLocaleString(n, s);
            })(t, s, this.qu.locale);
      }),
      (t.prototype.Ul = function (t) {
        var i = this.Xo;
        (this.Xo = t),
          Gi(i.jo(), this.Xo.jo()) || this.Jo.m(),
          Gi(i.qo(), this.Xo.qo()) || this.Go.m(),
          this.ql();
      }),
      (t.prototype.ql = function () {
        this.il = null;
      }),
      (t.prototype.ul = function () {
        this.ql(), this.Ko.clear();
      }),
      (t.prototype.rl = function () {
        var t = this.qu.dateFormat;
        this.zi.timeVisible
          ? (this.Il = new Xi({
              co: t,
              vo: this.zi.secondsVisible ? "%h:%m:%s" : "%h:%m",
              _o: "   ",
              do: this.qu.locale,
            }))
          : (this.Il = new Yi(t, this.qu.locale));
      }),
      (t.prototype.al = function () {
        if (this.zi.fixLeftEdge) {
          var t = this._l();
          if (null !== t) {
            var i = this.ss();
            if (null !== i) {
              var n = i.In() - t;
              if (n < 0) {
                var s = this.sl - n - 1;
                this.yn(s);
              }
              this.Ml();
            }
          }
        }
      }),
      (t.prototype.ol = function () {
        this.bl(), this.Ml();
      }),
      t
    );
  })();
  var hn,
    rn = (function (t) {
      function i(i) {
        var n = t.call(this) || this;
        return (n.Xl = new Map()), (n.Bt = i), n;
      }
      return (
        b(i, t),
        (i.prototype.Y = function (t) {}),
        (i.prototype.K = function (t) {
          if (this.Bt.yt) {
            t.save();
            for (var i = 0, n = 0, s = this.Bt.Zl; n < s.length; n++) {
              if (0 !== (a = s[n]).Gt.length) {
                t.font = a.T;
                var h = this.Jl(t, a.Gt);
                h > this.Bt.Ht ? (a.Al = this.Bt.Ht / h) : (a.Al = 1),
                  (i += a.Gl * a.Al);
              }
            }
            var r = 0;
            switch (this.Bt.Ql) {
              case "top":
                r = 0;
                break;
              case "center":
                r = Math.max((this.Bt.Yt - i) / 2, 0);
                break;
              case "bottom":
                r = Math.max(this.Bt.Yt - i, 0);
            }
            t.fillStyle = this.Bt.A;
            for (var e = 0, u = this.Bt.Zl; e < u.length; e++) {
              var a = u[e];
              t.save();
              var o = 0;
              switch (this.Bt.tf) {
                case "left":
                  (t.textAlign = "left"), (o = a.Gl / 2);
                  break;
                case "center":
                  (t.textAlign = "center"), (o = this.Bt.Ht / 2);
                  break;
                case "right":
                  (t.textAlign = "right"), (o = this.Bt.Ht - 1 - a.Gl / 2);
              }
              t.translate(o, r),
                (t.textBaseline = "top"),
                (t.font = a.T),
                t.scale(a.Al, a.Al),
                t.fillText(a.Gt, 0, a.if),
                t.restore(),
                (r += a.Gl * a.Al);
            }
            t.restore();
          }
        }),
        (i.prototype.Jl = function (t, i) {
          var n = this.nf(t.font),
            s = n.get(i);
          return void 0 === s && ((s = t.measureText(i).width), n.set(i, s)), s;
        }),
        (i.prototype.nf = function (t) {
          var i = this.Xl.get(t);
          return void 0 === i && ((i = new Map()), this.Xl.set(t, i)), i;
        }),
        i
      );
    })(O),
    en = (function () {
      function t(t) {
        (this.ft = !0),
          (this.Rt = {
            yt: !1,
            A: "",
            Yt: 0,
            Ht: 0,
            Zl: [],
            Ql: "center",
            tf: "center",
          }),
          (this.zt = new rn(this.Rt)),
          (this.Wt = t);
      }
      return (
        (t.prototype.vt = function () {
          this.ft = !0;
        }),
        (t.prototype.dt = function (t, i) {
          return this.ft && (this.wt(t, i), (this.ft = !1)), this.zt;
        }),
        (t.prototype.wt = function (t, i) {
          var n = this.Wt.R(),
            s = this.Rt;
          (s.yt = n.visible),
            s.yt &&
              ((s.A = n.color),
              (s.Ht = i),
              (s.Yt = t),
              (s.tf = n.horzAlign),
              (s.Ql = n.vertAlign),
              (s.Zl = [
                {
                  Gt: n.text,
                  T: B(n.fontSize, n.fontFamily, n.fontStyle),
                  Gl: 1.2 * n.fontSize,
                  if: 0,
                  Al: 0,
                },
              ]));
        }),
        t
      );
    })(),
    un = (function (t) {
      function i(i, n) {
        var s = t.call(this) || this;
        return (s.zi = n), (s.Hi = new en(s)), s;
      }
      return (
        b(i, t),
        (i.prototype.nn = function () {
          return [];
        }),
        (i.prototype.tn = function () {
          return [this.Hi];
        }),
        (i.prototype.R = function () {
          return this.zi;
        }),
        (i.prototype.hn = function () {
          this.Hi.vt();
        }),
        i
      );
    })(G);
  !(function (t) {
    (t[(t.OnTouchEnd = 0)] = "OnTouchEnd"),
      (t[(t.OnNextTap = 1)] = "OnNextTap");
  })(hn || (hn = {}));
  var an,
    on,
    ln,
    fn = (function () {
      function t(t, i) {
        (this.sf = []),
          (this.hf = []),
          (this.hh = 0),
          (this.rf = null),
          (this.ef = null),
          (this.uf = new p()),
          (this.af = new p()),
          (this.lf = null),
          (this.ff = t),
          (this.zi = i),
          (this.cf = new L(this)),
          (this.Da = new sn(this, i.timeScale, this.zi.localization)),
          (this.ct = new Q(this, i.crosshair)),
          (this.vf = new yi(i.crosshair)),
          (this._f = new un(this, i.watermark)),
          this.df(),
          this.sf[0].za(2e3),
          (this.wf = this.Mf(0)),
          (this.bf = this.Mf(1));
      }
      return (
        (t.prototype.Ce = function () {
          this.mf(new it(3));
        }),
        (t.prototype.Rr = function () {
          this.mf(new it(2));
        }),
        (t.prototype.Re = function () {
          this.mf(new it(1));
        }),
        (t.prototype.Se = function (t) {
          var i = this.gf(t);
          this.mf(i);
        }),
        (t.prototype.pf = function () {
          return this.ef;
        }),
        (t.prototype.yf = function (t) {
          var i = this.ef;
          (this.ef = t),
            null !== i && this.Se(i.kf),
            null !== t && this.Se(t.kf);
        }),
        (t.prototype.R = function () {
          return this.zi;
        }),
        (t.prototype.Pr = function (t) {
          y(this.zi, t),
            this.sf.forEach(function (i) {
              return i.Fa(t);
            }),
            void 0 !== t.timeScale && this.Da.Pr(t.timeScale),
            void 0 !== t.localization && this.Da.el(t.localization),
            (t.leftPriceScale || t.rightPriceScale) && this.uf.m(),
            (this.wf = this.Mf(0)),
            (this.bf = this.Mf(1)),
            this.Ce();
        }),
        (t.prototype.xf = function (t, i) {
          if ("left" !== t)
            if ("right" !== t) {
              var n = this.Nf(t);
              null !== n && (n.Ct.Pr(i), this.uf.m());
            } else this.Pr({ rightPriceScale: i });
          else this.Pr({ leftPriceScale: i });
        }),
        (t.prototype.Nf = function (t) {
          for (var i = 0, n = this.sf; i < n.length; i++) {
            var s = n[i],
              h = s.Va(t);
            if (null !== h) return { It: s, Ct: h };
          }
          return null;
        }),
        (t.prototype.bt = function () {
          return this.Da;
        }),
        (t.prototype.Cf = function () {
          return this.sf;
        }),
        (t.prototype.Sf = function () {
          return this._f;
        }),
        (t.prototype.Tf = function () {
          return this.ct;
        }),
        (t.prototype.Df = function () {
          return this.af;
        }),
        (t.prototype.Af = function (t, i) {
          t.ia(i), this.yl();
        }),
        (t.prototype.Wa = function (t) {
          (this.hh = t),
            this.Da.Wa(this.hh),
            this.sf.forEach(function (i) {
              return i.Wa(t);
            }),
            this.yl();
        }),
        (t.prototype.df = function (t) {
          var i = new qi(this.Da, this);
          void 0 !== t ? this.sf.splice(t, 0, i) : this.sf.push(i);
          var n = void 0 === t ? this.sf.length - 1 : t,
            s = new it(3);
          return s.cn(n, { vn: 0, _n: !0 }), this.mf(s), i;
        }),
        (t.prototype.Ka = function (t, i, n) {
          t.Ka(i, n);
        }),
        (t.prototype.Xa = function (t, i, n) {
          t.Xa(i, n), this.Te(), this.mf(this.Bf(t, 2));
        }),
        (t.prototype.Za = function (t, i) {
          t.Za(i), this.mf(this.Bf(t, 2));
        }),
        (t.prototype.Ja = function (t, i, n) {
          i.Xu() || t.Ja(i, n);
        }),
        (t.prototype.Ga = function (t, i, n) {
          i.Xu() || (t.Ga(i, n), this.Te(), this.mf(this.Bf(t, 2)));
        }),
        (t.prototype.Qa = function (t, i) {
          i.Xu() || (t.Qa(i), this.mf(this.Bf(t, 2)));
        }),
        (t.prototype.no = function (t, i) {
          t.no(i), this.mf(this.Bf(t, 2));
        }),
        (t.prototype.Lf = function (t) {
          this.Da.da(t);
        }),
        (t.prototype.Ef = function (t, i) {
          var n = this.bt();
          if (!n.wi() && 0 !== i) {
            var s = n.Ht();
            (t = Math.max(1, Math.min(t, s))), n.Al(t, i), this.yl();
          }
        }),
        (t.prototype.Of = function (t) {
          this.Ff(0), this.Vf(t), this.Pf();
        }),
        (t.prototype.Rf = function (t) {
          this.Da.wa(t), this.yl();
        }),
        (t.prototype.zf = function () {
          this.Da.Ma(), this.Rr();
        }),
        (t.prototype.Ff = function (t) {
          (this.rf = t), this.Da.ba(t);
        }),
        (t.prototype.Vf = function (t) {
          var i = !1;
          return (
            null !== this.rf &&
              Math.abs(t - this.rf) > 20 &&
              ((this.rf = null), (i = !0)),
            this.Da.ma(t),
            this.yl(),
            i
          );
        }),
        (t.prototype.Pf = function () {
          this.Da.ga(), this.Rr(), (this.rf = null);
        }),
        (t.prototype._t = function () {
          return this.hf;
        }),
        (t.prototype.Wf = function (t, i, n) {
          this.ct.Yi(t, i);
          var s = NaN,
            h = this.Da.gl(t),
            r = this.Da.ss();
          null !== r && (h = Math.min(Math.max(r.In(), h), r.jn()));
          var e = n.ji(),
            u = e.kt();
          null !== u && (s = e.qi(i, u)),
            (s = this.vf.Je(s, h, n)),
            this.ct.Zi(h, s, n),
            this.Re(),
            this.af.m(this.ct.Mt(), { x: t, y: i });
        }),
        (t.prototype.If = function () {
          this.Tf().Gi(), this.Re(), this.af.m(null, null);
        }),
        (t.prototype.Te = function () {
          var t = this.ct.It();
          if (null !== t) {
            var i = this.ct.Ki(),
              n = this.ct.Xi();
            this.Wf(i, n, t);
          }
          this.ct.hn();
        }),
        (t.prototype.jf = function (t, i, n) {
          var s = this.Da.pi(0);
          void 0 !== i && void 0 !== n && this.Da.vt(i, n);
          var h = this.Da.pi(0),
            r = this.Da.ml(),
            e = this.Da.ss();
          if (null !== e && null !== s && null !== h) {
            var u = e.Uh(r),
              a = s.So > h.So,
              o = null !== t && t > r && !a,
              l = u && this.Da.R().shiftVisibleRangeOnNewBar;
            if (o && !l) {
              var f = t - r;
              this.Da.yn(this.Da.xl() - f);
            }
          }
          this.Da.Dl(t);
        }),
        (t.prototype.Be = function (t) {
          null !== t && t.ho();
        }),
        (t.prototype.oh = function (t) {
          var i = this.sf.find(function (i) {
            return i.oa().includes(t);
          });
          return void 0 === i ? null : i;
        }),
        (t.prototype.yl = function () {
          this._f.hn(),
            this.sf.forEach(function (t) {
              return t.ho();
            }),
            this.Te();
        }),
        (t.prototype.p = function () {
          this.sf.forEach(function (t) {
            return t.p();
          }),
            (this.sf.length = 0),
            (this.zi.localization.priceFormatter = void 0),
            (this.zi.localization.timeFormatter = void 0);
        }),
        (t.prototype.qf = function () {
          return this.cf;
        }),
        (t.prototype.dh = function () {
          return this.cf.R();
        }),
        (t.prototype.Pa = function () {
          return this.uf;
        }),
        (t.prototype.Uf = function (t, i) {
          var n = this.sf[0],
            s = this.Hf(i, t, n);
          return (
            this.hf.push(s), 1 === this.hf.length ? this.Ce() : this.Rr(), s
          );
        }),
        (t.prototype.Yf = function (t) {
          var i = this.oh(t),
            n = this.hf.indexOf(t);
          h(-1 !== n, "Series not found"),
            this.hf.splice(n, 1),
            e(i).ca(t),
            t.p && t.p();
        }),
        (t.prototype.Ne = function (t, i) {
          var n = e(this.oh(t));
          n.ca(t);
          var s = this.Nf(i);
          if (null === s) {
            var h = t.Ni();
            n.la(t, i, h);
          } else {
            h = s.It === n ? t.Ni() : void 0;
            s.It.la(t, i, h);
          }
        }),
        (t.prototype.zl = function () {
          var t = new it(2);
          t.Mn(), this.mf(t);
        }),
        (t.prototype.$f = function (t) {
          var i = new it(2);
          i.mn(t), this.mf(i);
        }),
        (t.prototype.gn = function () {
          var t = new it(2);
          t.gn(), this.mf(t);
        }),
        (t.prototype.pn = function (t) {
          var i = new it(2);
          i.pn(t), this.mf(i);
        }),
        (t.prototype.yn = function (t) {
          var i = new it(2);
          i.yn(t), this.mf(i);
        }),
        (t.prototype.Kf = function () {
          return this.zi.rightPriceScale.visible ? "right" : "left";
        }),
        (t.prototype.Xf = function () {
          return this.bf;
        }),
        (t.prototype.Zf = function () {
          return this.wf;
        }),
        (t.prototype.Dt = function (t) {
          var i = this.bf,
            n = this.wf;
          if (i === n) return i;
          if (
            ((t = Math.max(0, Math.min(100, Math.round(100 * t)))),
            null === this.lf || this.lf.Pn !== n || this.lf.Rn !== i)
          )
            this.lf = { Pn: n, Rn: i, Jf: new Map() };
          else {
            var s = this.lf.Jf.get(t);
            if (void 0 !== s) return s;
          }
          var h = (function (t, i, n) {
            var s = d(t),
              h = s[0],
              r = s[1],
              e = s[2],
              u = s[3],
              a = d(i),
              f = a[0],
              c = a[1],
              v = a[2],
              _ = a[3],
              w = [
                o(h + n * (f - h)),
                o(r + n * (c - r)),
                o(e + n * (v - e)),
                l(u + n * (_ - u)),
              ];
            return "rgba("
              .concat(w[0], ", ")
              .concat(w[1], ", ")
              .concat(w[2], ", ")
              .concat(w[3], ")");
          })(n, i, t / 100);
          return this.lf.Jf.set(t, h), h;
        }),
        (t.prototype.Bf = function (t, i) {
          var n = new it(i);
          if (null !== t) {
            var s = this.sf.indexOf(t);
            n.cn(s, { vn: i });
          }
          return n;
        }),
        (t.prototype.gf = function (t, i) {
          return void 0 === i && (i = 2), this.Bf(this.oh(t), i);
        }),
        (t.prototype.mf = function (t) {
          this.ff && this.ff(t),
            this.sf.forEach(function (t) {
              return t.eo().ou().vt();
            });
        }),
        (t.prototype.Hf = function (t, i, n) {
          var s = new pi(this, t, i),
            h = void 0 !== t.priceScaleId ? t.priceScaleId : this.Kf();
          return n.la(s, h), tt(h) || s.Pr(t), s;
        }),
        (t.prototype.Mf = function (t) {
          var i = this.zi.layout;
          return "gradient" === i.background.type
            ? 0 === t
              ? i.background.topColor
              : i.background.bottomColor
            : i.background.color;
        }),
        t
      );
    })();
  function cn(t) {
    void 0 !== t.borderColor &&
      ((t.borderUpColor = t.borderColor), (t.borderDownColor = t.borderColor)),
      void 0 !== t.wickColor &&
        ((t.wickUpColor = t.wickColor), (t.wickDownColor = t.wickColor));
  }
  function vn(t) {
    return !k(t) && !N(t);
  }
  function _n(t) {
    return k(t);
  }
  !(function (t) {
    (t[(t.Disabled = 0)] = "Disabled"),
      (t[(t.Continuous = 1)] = "Continuous"),
      (t[(t.OnDataUpdate = 2)] = "OnDataUpdate");
  })(an || (an = {})),
    (function (t) {
      (t[(t.LastBar = 0)] = "LastBar"),
        (t[(t.LastVisible = 1)] = "LastVisible");
    })(on || (on = {})),
    (function (t) {
      (t.Solid = "solid"), (t.VerticalGradient = "gradient");
    })(ln || (ln = {}));
  var dn = { allowDownsampling: !0 };
  var wn = (function () {
      function t(t, i) {
        var n = this;
        (this._resolutionMediaQueryList = null),
          (this._resolutionListener = function (t) {
            return n._onResolutionChanged();
          }),
          (this._canvasConfiguredListeners = []),
          (this.canvas = t),
          (this._canvasSize = {
            width: this.canvas.clientWidth,
            height: this.canvas.clientHeight,
          }),
          (this._options = i),
          this._configureCanvas(),
          this._installResolutionListener();
      }
      return (
        (t.prototype.destroy = function () {
          (this._canvasConfiguredListeners.length = 0),
            this._uninstallResolutionListener(),
            (this.canvas = null);
        }),
        Object.defineProperty(t.prototype, "canvasSize", {
          get: function () {
            return {
              width: this._canvasSize.width,
              height: this._canvasSize.height,
            };
          },
          enumerable: !0,
          configurable: !0,
        }),
        (t.prototype.resizeCanvas = function (t) {
          (this._canvasSize = { width: t.width, height: t.height }),
            this._configureCanvas();
        }),
        Object.defineProperty(t.prototype, "pixelRatio", {
          get: function () {
            var t = this.canvas.ownerDocument.defaultView;
            if (null == t)
              throw new Error("No window is associated with the canvas");
            return t.devicePixelRatio > 1 || this._options.allowDownsampling
              ? t.devicePixelRatio
              : 1;
          },
          enumerable: !0,
          configurable: !0,
        }),
        (t.prototype.subscribeCanvasConfigured = function (t) {
          this._canvasConfiguredListeners.push(t);
        }),
        (t.prototype.unsubscribeCanvasConfigured = function (t) {
          this._canvasConfiguredListeners =
            this._canvasConfiguredListeners.filter(function (i) {
              return i != t;
            });
        }),
        (t.prototype._configureCanvas = function () {
          var t = this.pixelRatio;
          (this.canvas.style.width = this._canvasSize.width + "px"),
            (this.canvas.style.height = this._canvasSize.height + "px"),
            (this.canvas.width = this._canvasSize.width * t),
            (this.canvas.height = this._canvasSize.height * t),
            this._emitCanvasConfigured();
        }),
        (t.prototype._emitCanvasConfigured = function () {
          var t = this;
          this._canvasConfiguredListeners.forEach(function (i) {
            return i.call(t);
          });
        }),
        (t.prototype._installResolutionListener = function () {
          if (null !== this._resolutionMediaQueryList)
            throw new Error("Resolution listener is already installed");
          var t = this.canvas.ownerDocument.defaultView;
          if (null == t)
            throw new Error("No window is associated with the canvas");
          var i = t.devicePixelRatio;
          (this._resolutionMediaQueryList = t.matchMedia(
            "all and (resolution: " + i + "dppx)"
          )),
            this._resolutionMediaQueryList.addListener(
              this._resolutionListener
            );
        }),
        (t.prototype._uninstallResolutionListener = function () {
          null !== this._resolutionMediaQueryList &&
            (this._resolutionMediaQueryList.removeListener(
              this._resolutionListener
            ),
            (this._resolutionMediaQueryList = null));
        }),
        (t.prototype._reinstallResolutionListener = function () {
          this._uninstallResolutionListener(),
            this._installResolutionListener();
        }),
        (t.prototype._onResolutionChanged = function () {
          this._configureCanvas(), this._reinstallResolutionListener();
        }),
        t
      );
    })(),
    Mn = (function () {
      function t(t, i) {
        (this.Ot = t), (this.Ft = i);
      }
      return (
        (t.prototype.br = function (t) {
          return this.Ot === t.Ot && this.Ft === t.Ft;
        }),
        t
      );
    })();
  function bn(t) {
    return (
      (t.ownerDocument &&
        t.ownerDocument.defaultView &&
        t.ownerDocument.defaultView.devicePixelRatio) ||
      1
    );
  }
  function mn(t) {
    var i = e(t.getContext("2d"));
    return i.setTransform(1, 0, 0, 1, 0, 0), i;
  }
  function gn(t, i) {
    var n = t.createElement("canvas"),
      s = bn(n);
    return (
      (n.style.width = "".concat(i.Ot, "px")),
      (n.style.height = "".concat(i.Ft, "px")),
      (n.width = i.Ot * s),
      (n.height = i.Ft * s),
      n
    );
  }
  function pn(t, i) {
    var n = e(t.ownerDocument).createElement("canvas");
    t.appendChild(n);
    var s = (function (t, i) {
      return void 0 === i && (i = dn), new wn(t, i);
    })(n, { allowDownsampling: !1 });
    return s.resizeCanvas({ width: i.Ot, height: i.Ft }), s;
  }
  function yn(t, i) {
    return t.Gf - i.Gf;
  }
  function kn(t, i, n) {
    var s = (t.Gf - i.Gf) / (t.rt - i.rt);
    return Math.sign(s) * Math.min(Math.abs(s), n);
  }
  var xn = (function () {
      function t(t, i, n, s) {
        (this.Qf = null),
          (this.tc = null),
          (this.ic = null),
          (this.nc = null),
          (this.sc = null),
          (this.hc = 0),
          (this.rc = 0),
          (this.ec = !1),
          (this.uc = t),
          (this.ac = i),
          (this.oc = n),
          (this.Cn = s);
      }
      return (
        (t.prototype.lc = function (t, i) {
          if (null !== this.Qf) {
            if (this.Qf.rt === i) return void (this.Qf.Gf = t);
            if (Math.abs(this.Qf.Gf - t) < this.Cn) return;
          }
          (this.nc = this.ic),
            (this.ic = this.tc),
            (this.tc = this.Qf),
            (this.Qf = { rt: i, Gf: t });
        }),
        (t.prototype.Nh = function (t, i) {
          if (null !== this.Qf && null !== this.tc && !(i - this.Qf.rt > 50)) {
            var n = 0,
              s = kn(this.Qf, this.tc, this.ac),
              h = yn(this.Qf, this.tc),
              r = [s],
              e = [h];
            if (((n += h), null !== this.ic)) {
              var u = kn(this.tc, this.ic, this.ac);
              if (Math.sign(u) === Math.sign(s)) {
                var a = yn(this.tc, this.ic);
                if ((r.push(u), e.push(a), (n += a), null !== this.nc)) {
                  var o = kn(this.ic, this.nc, this.ac);
                  if (Math.sign(o) === Math.sign(s)) {
                    var l = yn(this.ic, this.nc);
                    r.push(o), e.push(l), (n += l);
                  }
                }
              }
            }
            for (var f, c, v, _ = 0, d = 0; d < r.length; ++d)
              _ += (e[d] / n) * r[d];
            if (!(Math.abs(_) < this.uc))
              (this.sc = { Gf: t, rt: i }),
                (this.rc = _),
                (this.hc =
                  ((f = Math.abs(_)),
                  (c = this.oc),
                  (v = Math.log(c)),
                  Math.log((1 * v) / -f) / v));
          }
        }),
        (t.prototype.fc = function (t) {
          var i = e(this.sc),
            n = t - i.rt;
          return (
            i.Gf + (this.rc * (Math.pow(this.oc, n) - 1)) / Math.log(this.oc)
          );
        }),
        (t.prototype.cc = function (t) {
          return null === this.sc || this.vc(t) === this.hc;
        }),
        (t.prototype._c = function () {
          return this.ec;
        }),
        (t.prototype.dc = function () {
          this.ec = !0;
        }),
        (t.prototype.vc = function (t) {
          var i = t - e(this.sc).rt;
          return Math.min(i, this.hc);
        }),
        t
      );
    })(),
    Nn = "undefined" != typeof window;
  function Cn() {
    return (
      !!Nn && window.navigator.userAgent.toLowerCase().indexOf("firefox") > -1
    );
  }
  function Sn() {
    return !!Nn && /iPhone|iPad|iPod/.test(window.navigator.platform);
  }
  function Tn(t) {
    Nn &&
      void 0 !== window.chrome &&
      t.addEventListener("mousedown", function (t) {
        if (1 === t.button) return t.preventDefault(), !1;
      });
  }
  var Dn = (function () {
    function t(t, i, n) {
      var s = this;
      (this.wc = 0),
        (this.Mc = null),
        (this.bc = {
          tt: Number.NEGATIVE_INFINITY,
          it: Number.POSITIVE_INFINITY,
        }),
        (this.mc = 0),
        (this.gc = null),
        (this.yc = {
          tt: Number.NEGATIVE_INFINITY,
          it: Number.POSITIVE_INFINITY,
        }),
        (this.kc = null),
        (this.xc = !1),
        (this.Nc = null),
        (this.Cc = null),
        (this.Sc = !1),
        (this.Tc = !1),
        (this.Dc = !1),
        (this.Ac = null),
        (this.Bc = null),
        (this.Lc = null),
        (this.Ec = null),
        (this.Oc = null),
        (this.Fc = null),
        (this.Vc = null),
        (this.Pc = 0),
        (this.Rc = !1),
        (this.zc = !1),
        (this.Wc = !1),
        (this.Ic = 0),
        (this.jc = null),
        (this.qc = !Sn()),
        (this.Uc = function (t) {
          s.Hc(t);
        }),
        (this.Yc = function (t) {
          if (s.$c(t)) {
            var i = s.Kc(t);
            if ((++s.mc, s.gc && s.mc > 1))
              s.Zc(Ln(t), s.yc).Xc < 30 && !s.Dc && s.Jc(i, s.Qc.Gc), s.tv();
          } else {
            i = s.Kc(t);
            if ((++s.wc, s.Mc && s.wc > 1))
              s.Zc(Ln(t), s.bc).Xc < 5 && !s.Tc && s.iv(i, s.Qc.nv), s.sv();
          }
        }),
        (this.hv = t),
        (this.Qc = i),
        (this.zi = n),
        this.rv();
    }
    return (
      (t.prototype.p = function () {
        null !== this.Ac && (this.Ac(), (this.Ac = null)),
          null !== this.Bc && (this.Bc(), (this.Bc = null)),
          null !== this.Ec && (this.Ec(), (this.Ec = null)),
          null !== this.Oc && (this.Oc(), (this.Oc = null)),
          null !== this.Fc && (this.Fc(), (this.Fc = null)),
          null !== this.Lc && (this.Lc(), (this.Lc = null)),
          this.ev(),
          this.sv();
      }),
      (t.prototype.uv = function (t) {
        var i = this;
        this.Ec && this.Ec();
        var n = this.av.bind(this);
        if (
          ((this.Ec = function () {
            i.hv.removeEventListener("mousemove", n);
          }),
          this.hv.addEventListener("mousemove", n),
          !this.$c(t))
        ) {
          var s = this.Kc(t);
          this.iv(s, this.Qc.ov), (this.qc = !0);
        }
      }),
      (t.prototype.sv = function () {
        null !== this.Mc && clearTimeout(this.Mc),
          (this.wc = 0),
          (this.Mc = null),
          (this.bc = {
            tt: Number.NEGATIVE_INFINITY,
            it: Number.POSITIVE_INFINITY,
          });
      }),
      (t.prototype.tv = function () {
        null !== this.gc && clearTimeout(this.gc),
          (this.mc = 0),
          (this.gc = null),
          (this.yc = {
            tt: Number.NEGATIVE_INFINITY,
            it: Number.POSITIVE_INFINITY,
          });
      }),
      (t.prototype.av = function (t) {
        if (!this.Wc && null === this.Cc && !this.$c(t)) {
          var i = this.Kc(t);
          this.iv(i, this.Qc.lv), (this.qc = !0);
        }
      }),
      (t.prototype.fv = function (t) {
        var i = On(t.changedTouches, e(this.jc));
        if (null !== i && ((this.Ic = En(t)), null === this.Vc && !this.zc)) {
          this.Rc = !0;
          var n = this.Zc(Ln(i), e(this.Cc)),
            s = n.cv,
            h = n.vv,
            r = n.Xc;
          if (this.Sc || !(r < 5)) {
            if (!this.Sc) {
              var u = 0.5 * s,
                a = h >= u && !this.zi._v(),
                o = u > h && !this.zi.dv();
              a || o || (this.zc = !0),
                (this.Sc = !0),
                (this.Dc = !0),
                this.ev(),
                this.tv();
            }
            if (!this.zc) {
              var l = this.Kc(t, i);
              this.Jc(l, this.Qc.wv), Bn(t);
            }
          }
        }
      }),
      (t.prototype.Mv = function (t) {
        if (
          0 === t.button &&
          (this.Zc(Ln(t), e(this.Nc)).Xc >= 5 && ((this.Tc = !0), this.sv()),
          this.Tc)
        ) {
          var i = this.Kc(t);
          this.iv(i, this.Qc.bv);
        }
      }),
      (t.prototype.Zc = function (t, i) {
        var n = Math.abs(i.tt - t.tt),
          s = Math.abs(i.it - t.it);
        return { cv: n, vv: s, Xc: n + s };
      }),
      (t.prototype.mv = function (t) {
        var i = On(t.changedTouches, e(this.jc));
        if (
          (null === i && 0 === t.touches.length && (i = t.changedTouches[0]),
          null !== i)
        ) {
          (this.jc = null),
            (this.Ic = En(t)),
            this.ev(),
            (this.Cc = null),
            this.Fc && (this.Fc(), (this.Fc = null));
          var n = this.Kc(t, i);
          if ((this.Jc(n, this.Qc.gv), ++this.mc, this.gc && this.mc > 1))
            this.Zc(Ln(i), this.yc).Xc < 30 &&
              !this.Dc &&
              this.Jc(n, this.Qc.Gc),
              this.tv();
          else this.Dc || (this.Jc(n, this.Qc.pv), this.Qc.pv && Bn(t));
          0 === this.mc && Bn(t),
            0 === t.touches.length && this.xc && ((this.xc = !1), Bn(t));
        }
      }),
      (t.prototype.Hc = function (t) {
        if (0 === t.button) {
          var i = this.Kc(t);
          if (
            ((this.Nc = null),
            (this.Wc = !1),
            this.Oc && (this.Oc(), (this.Oc = null)),
            Cn())
          )
            this.hv.ownerDocument.documentElement.removeEventListener(
              "mouseleave",
              this.Uc
            );
          if (!this.$c(t))
            if ((this.iv(i, this.Qc.yv), ++this.wc, this.Mc && this.wc > 1))
              this.Zc(Ln(t), this.bc).Xc < 5 &&
                !this.Tc &&
                this.iv(i, this.Qc.nv),
                this.sv();
            else this.Tc || this.iv(i, this.Qc.kv);
        }
      }),
      (t.prototype.ev = function () {
        null !== this.kc && (clearTimeout(this.kc), (this.kc = null));
      }),
      (t.prototype.xv = function (t) {
        if (null === this.jc) {
          var i = t.changedTouches[0];
          (this.jc = i.identifier), (this.Ic = En(t));
          var n = this.hv.ownerDocument.documentElement;
          (this.Dc = !1),
            (this.Sc = !1),
            (this.zc = !1),
            (this.Cc = Ln(i)),
            this.Fc && (this.Fc(), (this.Fc = null));
          var s = this.fv.bind(this),
            h = this.mv.bind(this);
          (this.Fc = function () {
            n.removeEventListener("touchmove", s),
              n.removeEventListener("touchend", h);
          }),
            n.addEventListener("touchmove", s, { passive: !1 }),
            n.addEventListener("touchend", h, { passive: !1 }),
            this.ev(),
            (this.kc = setTimeout(this.Nv.bind(this, t), 240));
          var r = this.Kc(t, i);
          this.Jc(r, this.Qc.Cv),
            this.gc ||
              ((this.mc = 0),
              (this.gc = setTimeout(this.tv.bind(this), 500)),
              (this.yc = Ln(i)));
        }
      }),
      (t.prototype.Sv = function (t) {
        if (0 === t.button) {
          var i = this.hv.ownerDocument.documentElement;
          Cn() && i.addEventListener("mouseleave", this.Uc),
            (this.Tc = !1),
            (this.Nc = Ln(t)),
            this.Oc && (this.Oc(), (this.Oc = null));
          var n = this.Mv.bind(this),
            s = this.Hc.bind(this);
          if (
            ((this.Oc = function () {
              i.removeEventListener("mousemove", n),
                i.removeEventListener("mouseup", s);
            }),
            i.addEventListener("mousemove", n),
            i.addEventListener("mouseup", s),
            (this.Wc = !0),
            !this.$c(t))
          ) {
            var h = this.Kc(t);
            this.iv(h, this.Qc.Tv),
              this.Mc ||
                ((this.wc = 0),
                (this.Mc = setTimeout(this.sv.bind(this), 500)),
                (this.bc = Ln(t)));
          }
        }
      }),
      (t.prototype.rv = function () {
        var t = this;
        this.hv.addEventListener("mouseenter", this.uv.bind(this)),
          this.hv.addEventListener("touchcancel", this.ev.bind(this));
        var i = this.hv.ownerDocument,
          n = function (i) {
            t.Qc.Dv && ((i.target && t.hv.contains(i.target)) || t.Qc.Dv());
          };
        (this.Bc = function () {
          i.removeEventListener("touchstart", n);
        }),
          (this.Ac = function () {
            i.removeEventListener("mousedown", n);
          }),
          i.addEventListener("mousedown", n),
          i.addEventListener("touchstart", n, { passive: !0 }),
          Sn() &&
            ((this.Lc = function () {
              t.hv.removeEventListener("dblclick", t.Yc);
            }),
            this.hv.addEventListener("dblclick", this.Yc)),
          this.hv.addEventListener("mouseleave", this.Av.bind(this)),
          this.hv.addEventListener("touchstart", this.xv.bind(this), {
            passive: !0,
          }),
          Tn(this.hv),
          this.hv.addEventListener("mousedown", this.Sv.bind(this)),
          this.Bv(),
          this.hv.addEventListener("touchmove", function () {}, {
            passive: !1,
          });
      }),
      (t.prototype.Bv = function () {
        var t = this;
        (void 0 === this.Qc.Lv &&
          void 0 === this.Qc.Ev &&
          void 0 === this.Qc.Ov) ||
          (this.hv.addEventListener(
            "touchstart",
            function (i) {
              return t.Fv(i.touches);
            },
            { passive: !0 }
          ),
          this.hv.addEventListener(
            "touchmove",
            function (i) {
              if (
                2 === i.touches.length &&
                null !== t.Vc &&
                void 0 !== t.Qc.Ev
              ) {
                var n = An(i.touches[0], i.touches[1]) / t.Pc;
                t.Qc.Ev(t.Vc, n), Bn(i);
              }
            },
            { passive: !1 }
          ),
          this.hv.addEventListener("touchend", function (i) {
            t.Fv(i.touches);
          }));
      }),
      (t.prototype.Fv = function (t) {
        1 === t.length && (this.Rc = !1),
          2 !== t.length || this.Rc || this.xc ? this.Vv() : this.Pv(t);
      }),
      (t.prototype.Pv = function (t) {
        var i = this.hv.getBoundingClientRect() || { left: 0, top: 0 };
        (this.Vc = {
          tt: (t[0].clientX - i.left + (t[1].clientX - i.left)) / 2,
          it: (t[0].clientY - i.top + (t[1].clientY - i.top)) / 2,
        }),
          (this.Pc = An(t[0], t[1])),
          void 0 !== this.Qc.Lv && this.Qc.Lv(),
          this.ev();
      }),
      (t.prototype.Vv = function () {
        null !== this.Vc &&
          ((this.Vc = null), void 0 !== this.Qc.Ov && this.Qc.Ov());
      }),
      (t.prototype.Av = function (t) {
        if ((this.Ec && this.Ec(), !this.$c(t) && this.qc)) {
          var i = this.Kc(t);
          this.iv(i, this.Qc.Rv), (this.qc = !Sn());
        }
      }),
      (t.prototype.Nv = function (t) {
        var i = On(t.touches, e(this.jc));
        if (null !== i) {
          var n = this.Kc(t, i);
          this.Jc(n, this.Qc.zv), (this.Dc = !0), (this.xc = !0);
        }
      }),
      (t.prototype.$c = function (t) {
        return t.sourceCapabilities &&
          void 0 !== t.sourceCapabilities.firesTouchEvents
          ? t.sourceCapabilities.firesTouchEvents
          : En(t) < this.Ic + 500;
      }),
      (t.prototype.Jc = function (t, i) {
        i && i.call(this.Qc, t);
      }),
      (t.prototype.iv = function (t, i) {
        i && i.call(this.Qc, t);
      }),
      (t.prototype.Kc = function (t, i) {
        var n = i || t,
          s = this.hv.getBoundingClientRect() || { left: 0, top: 0 };
        return {
          Wv: n.clientX,
          Iv: n.clientY,
          jv: n.pageX,
          qv: n.pageY,
          Uv: n.screenX,
          Hv: n.screenY,
          Yv: n.clientX - s.left,
          $v: n.clientY - s.top,
          Kv: t.ctrlKey,
          Xv: t.altKey,
          Zv: t.shiftKey,
          Jv: t.metaKey,
          Gv:
            !t.type.startsWith("mouse") &&
            "contextmenu" !== t.type &&
            "click" !== t.type,
          Qv: t.type,
          t_: n.target,
          i_: t.view,
          n_: function () {
            "touchstart" !== t.type && Bn(t);
          },
        };
      }),
      t
    );
  })();
  function An(t, i) {
    var n = t.clientX - i.clientX,
      s = t.clientY - i.clientY;
    return Math.sqrt(n * n + s * s);
  }
  function Bn(t) {
    t.cancelable && t.preventDefault();
  }
  function Ln(t) {
    return { tt: t.pageX, it: t.pageY };
  }
  function En(t) {
    return t.timeStamp || performance.now();
  }
  function On(t, i) {
    for (var n = 0; n < t.length; ++n) if (t[n].identifier === i) return t[n];
    return null;
  }
  var Fn = (function () {
      function t(t, i, n, s) {
        (this.rh = new zt(200)),
          (this.W = 0),
          (this.s_ = ""),
          (this.Yh = ""),
          (this.th = []),
          (this.h_ = new Map()),
          (this.W = t),
          (this.s_ = i),
          (this.Yh = B(t, n, s));
      }
      return (
        (t.prototype.p = function () {
          this.rh.ih(), (this.th = []), this.h_.clear();
        }),
        (t.prototype.r_ = function (t, i, n, s, h) {
          var r = this.e_(t, i);
          if ("left" !== h) {
            var e = bn(t.canvas);
            n -= Math.floor(r.u_ * e);
          }
          (s -= Math.floor(r.Yt / 2)), t.drawImage(r.a_, n, s, r.Ht, r.Yt);
        }),
        (t.prototype.e_ = function (t, i) {
          var n,
            s = this;
          if (this.h_.has(i)) n = r(this.h_.get(i));
          else {
            if (this.th.length >= 200) {
              var h = r(this.th.shift());
              this.h_.delete(h);
            }
            var e = bn(t.canvas),
              u = Math.ceil(this.W / 4.5),
              a = Math.round(this.W / 10),
              o = Math.ceil(this.rh.Qt(t, i)),
              l = Ct(Math.round(o + 2 * u)),
              f = Ct(this.W + 2 * u),
              c = gn(document, new Mn(l, f));
            (n = {
              Gt: i,
              u_: Math.round(Math.max(1, o)),
              Ht: Math.ceil(l * e),
              Yt: Math.ceil(f * e),
              a_: c,
            }),
              0 !== o && (this.th.push(n.Gt), this.h_.set(n.Gt, n)),
              j((t = mn(n.a_)), e, function () {
                (t.font = s.Yh),
                  (t.fillStyle = s.s_),
                  t.fillText(i, 0, f - u - a);
              });
          }
          return n;
        }),
        t
      );
    })(),
    Vn = (function () {
      function t(t, i, n, s) {
        var h = this;
        (this._i = null),
          (this.o_ = null),
          (this.l_ = !1),
          (this.f_ = new zt(50)),
          (this.c_ = new Fn(11, "#000")),
          (this.s_ = null),
          (this.Yh = null),
          (this.v_ = 0),
          (this.__ = !1),
          (this.d_ = function () {
            h.w_(h.cf.R()), h.__ || h.Di.M_().jt().Rr();
          }),
          (this.b_ = function () {
            h.__ || h.Di.M_().jt().Rr();
          }),
          (this.Di = t),
          (this.zi = i),
          (this.cf = n),
          (this.m_ = "left" === s),
          (this.g_ = document.createElement("div")),
          (this.g_.style.height = "100%"),
          (this.g_.style.overflow = "hidden"),
          (this.g_.style.width = "25px"),
          (this.g_.style.left = "0"),
          (this.g_.style.position = "relative"),
          (this.p_ = pn(this.g_, new Mn(16, 16))),
          this.p_.subscribeCanvasConfigured(this.d_);
        var r = this.p_.canvas;
        (r.style.position = "absolute"),
          (r.style.zIndex = "1"),
          (r.style.left = "0"),
          (r.style.top = "0"),
          (this.y_ = pn(this.g_, new Mn(16, 16))),
          this.y_.subscribeCanvasConfigured(this.b_);
        var e = this.y_.canvas;
        (e.style.position = "absolute"),
          (e.style.zIndex = "2"),
          (e.style.left = "0"),
          (e.style.top = "0");
        var u = {
          Tv: this.k_.bind(this),
          Cv: this.k_.bind(this),
          bv: this.x_.bind(this),
          wv: this.x_.bind(this),
          Dv: this.N_.bind(this),
          yv: this.C_.bind(this),
          gv: this.C_.bind(this),
          nv: this.S_.bind(this),
          Gc: this.S_.bind(this),
          ov: this.T_.bind(this),
          Rv: this.D_.bind(this),
        };
        this.A_ = new Dn(this.y_.canvas, u, {
          _v: function () {
            return !1;
          },
          dv: function () {
            return !0;
          },
        });
      }
      return (
        (t.prototype.p = function () {
          this.A_.p(),
            this.y_.unsubscribeCanvasConfigured(this.b_),
            this.y_.destroy(),
            this.p_.unsubscribeCanvasConfigured(this.d_),
            this.p_.destroy(),
            null !== this._i && this._i._a().M(this),
            (this._i = null),
            this.c_.p();
        }),
        (t.prototype.B_ = function () {
          return this.g_;
        }),
        (t.prototype.ht = function () {
          return e(this._i).R().borderColor;
        }),
        (t.prototype.L_ = function () {
          return this.zi.textColor;
        }),
        (t.prototype.S = function () {
          return this.zi.fontSize;
        }),
        (t.prototype.E_ = function () {
          return B(this.S(), this.zi.fontFamily);
        }),
        (t.prototype.O_ = function () {
          var t = this.cf.R(),
            i = this.s_ !== t.A,
            n = this.Yh !== t.T;
          return (
            (i || n) && (this.w_(t), (this.s_ = t.A)),
            n && (this.f_.ih(), (this.Yh = t.T)),
            t
          );
        }),
        (t.prototype.F_ = function () {
          if (null === this._i) return 0;
          var t = 0,
            i = this.O_(),
            n = mn(this.p_.canvas),
            s = this._i.au();
          (n.font = this.E_()),
            s.length > 0 &&
              (t = Math.max(
                this.f_.Qt(n, s[0].yu),
                this.f_.Qt(n, s[s.length - 1].yu)
              ));
          for (var h = this.V_(), r = h.length; r--; ) {
            var e = this.f_.Qt(n, h[r].Gt());
            e > t && (t = e);
          }
          var u = this._i.kt();
          if (null !== u && null !== this.o_) {
            var a = this._i.qi(1, u),
              o = this._i.qi(this.o_.Ft - 2, u);
            t = Math.max(
              t,
              this.f_.Qt(
                n,
                this._i.Mi(Math.floor(Math.min(a, o)) + 0.11111111111111, u)
              ),
              this.f_.Qt(
                n,
                this._i.Mi(Math.ceil(Math.max(a, o)) - 0.11111111111111, u)
              )
            );
          }
          var l = t || 34,
            f = Math.ceil(i.N + i.C + i.L + i.O + l);
          return (f += f % 2);
        }),
        (t.prototype.P_ = function (t) {
          if (t.Ot < 0 || t.Ft < 0)
            throw new Error(
              "Try to set invalid size to PriceAxisWidget " + JSON.stringify(t)
            );
          (null !== this.o_ && this.o_.br(t)) ||
            ((this.o_ = t),
            (this.__ = !0),
            this.p_.resizeCanvas({ width: t.Ot, height: t.Ft }),
            this.y_.resizeCanvas({ width: t.Ot, height: t.Ft }),
            (this.__ = !1),
            (this.g_.style.width = t.Ot + "px"),
            (this.g_.style.height = t.Ft + "px"),
            (this.g_.style.minWidth = t.Ot + "px"));
        }),
        (t.prototype.R_ = function () {
          return e(this.o_).Ot;
        }),
        (t.prototype.Si = function (t) {
          this._i !== t &&
            (null !== this._i && this._i._a().M(this),
            (this._i = t),
            t._a().u(this.Eu.bind(this), this));
        }),
        (t.prototype.Ct = function () {
          return this._i;
        }),
        (t.prototype.ih = function () {
          var t = this.Di.z_();
          this.Di.M_().jt().no(t, e(this.Ct()));
        }),
        (t.prototype.W_ = function (t) {
          if (null !== this.o_) {
            if (1 !== t) {
              var i = mn(this.p_.canvas);
              this.I_(),
                this.j_(i, this.p_.pixelRatio),
                this.Ws(i, this.p_.pixelRatio),
                this.q_(i, this.p_.pixelRatio),
                this.U_(i, this.p_.pixelRatio);
            }
            var n = mn(this.y_.canvas),
              s = this.o_.Ot,
              h = this.o_.Ft;
            j(n, this.y_.pixelRatio, function () {
              n.clearRect(0, 0, s, h);
            }),
              this.H_(n, this.y_.pixelRatio);
          }
        }),
        (t.prototype.Y_ = function () {
          return this.p_.canvas;
        }),
        (t.prototype.vt = function () {
          var t;
          null === (t = this._i) || void 0 === t || t.au();
        }),
        (t.prototype.k_ = function (t) {
          if (
            null !== this._i &&
            !this._i.wi() &&
            this.Di.M_().R().handleScale.axisPressedMouseMove.price
          ) {
            var i = this.Di.M_().jt(),
              n = this.Di.z_();
            (this.l_ = !0), i.Ka(n, this._i, t.$v);
          }
        }),
        (t.prototype.x_ = function (t) {
          if (
            null !== this._i &&
            this.Di.M_().R().handleScale.axisPressedMouseMove.price
          ) {
            var i = this.Di.M_().jt(),
              n = this.Di.z_(),
              s = this._i;
            i.Xa(n, s, t.$v);
          }
        }),
        (t.prototype.N_ = function () {
          if (
            null !== this._i &&
            this.Di.M_().R().handleScale.axisPressedMouseMove.price
          ) {
            var t = this.Di.M_().jt(),
              i = this.Di.z_(),
              n = this._i;
            this.l_ && ((this.l_ = !1), t.Za(i, n));
          }
        }),
        (t.prototype.C_ = function (t) {
          if (
            null !== this._i &&
            this.Di.M_().R().handleScale.axisPressedMouseMove.price
          ) {
            var i = this.Di.M_().jt(),
              n = this.Di.z_();
            (this.l_ = !1), i.Za(n, this._i);
          }
        }),
        (t.prototype.S_ = function (t) {
          this.Di.M_().R().handleScale.axisDoubleClickReset && this.ih();
        }),
        (t.prototype.T_ = function (t) {
          null !== this._i &&
            (!this.Di.M_().jt().R().handleScale.axisPressedMouseMove.price ||
              this._i.vr() ||
              this._i.Zu() ||
              this.K_(1));
        }),
        (t.prototype.D_ = function (t) {
          this.K_(0);
        }),
        (t.prototype.V_ = function () {
          var t = this,
            i = [],
            n = null === this._i ? void 0 : this._i;
          return (
            (function (s) {
              for (var h = 0; h < s.length; ++h)
                for (var r = s[h].nn(t.Di.z_(), n), e = 0; e < r.length; e++)
                  i.push(r[e]);
            })(this.Di.z_().oa()),
            i
          );
        }),
        (t.prototype.j_ = function (t, i) {
          var n = this;
          if (null !== this.o_) {
            var s = this.o_.Ot,
              h = this.o_.Ft;
            j(t, i, function () {
              var i = n.Di.z_().jt(),
                r = i.Zf(),
                e = i.Xf();
              r === e ? q(t, 0, 0, s, h, r) : U(t, 0, 0, s, h, r, e);
            });
          }
        }),
        (t.prototype.Ws = function (t, i) {
          if (
            null !== this.o_ &&
            null !== this._i &&
            this._i.R().borderVisible
          ) {
            t.save(), (t.fillStyle = this.ht());
            var n,
              s = Math.max(1, Math.floor(this.O_().N * i));
            (n = this.m_ ? Math.floor(this.o_.Ot * i) - s : 0),
              t.fillRect(n, 0, s, Math.ceil(this.o_.Ft * i)),
              t.restore();
          }
        }),
        (t.prototype.q_ = function (t, i) {
          if (null !== this.o_ && null !== this._i) {
            var n = this._i.au();
            t.save(),
              (t.strokeStyle = this.ht()),
              (t.font = this.E_()),
              (t.fillStyle = this.ht());
            var s = this.O_(),
              h = this._i.R().borderVisible && this._i.R().drawTicks,
              r = this.m_
                ? Math.floor((this.o_.Ot - s.C) * i - s.N * i)
                : Math.floor(s.N * i),
              e = this.m_
                ? Math.round(r - s.L * i)
                : Math.round(r + s.C * i + s.L * i),
              u = this.m_ ? "right" : "left",
              a = Math.max(1, Math.floor(i)),
              o = Math.floor(0.5 * i);
            if (h) {
              var l = Math.round(s.C * i);
              t.beginPath();
              for (var f = 0, c = n; f < c.length; f++) {
                var v = c[f];
                t.rect(r, Math.round(v.su * i) - o, l, a);
              }
              t.fill();
            }
            t.fillStyle = this.L_();
            for (var _ = 0, d = n; _ < d.length; _++) {
              v = d[_];
              this.c_.r_(t, v.yu, e, Math.round(v.su * i), u);
            }
            t.restore();
          }
        }),
        (t.prototype.I_ = function () {
          if (null !== this.o_ && null !== this._i) {
            var t = this.o_.Ft / 2,
              i = [],
              n = this._i.oa().slice(),
              s = this.Di.z_(),
              h = this.O_();
            this._i === s.fh() &&
              this.Di.z_()
                .oa()
                .forEach(function (t) {
                  s.lh(t) && n.push(t);
                });
            var r = this._i.Ge()[0],
              e = this._i;
            n.forEach(function (n) {
              var h = n.nn(s, e);
              h.forEach(function (t) {
                t.oi(null), t.li() && i.push(t);
              }),
                r === n && h.length > 0 && (t = h[0].ti());
            });
            var u = i.filter(function (i) {
                return i.ti() <= t;
              }),
              a = i.filter(function (i) {
                return i.ti() > t;
              });
            if (
              (u.sort(function (t, i) {
                return i.ti() - t.ti();
              }),
              u.length && a.length && a.push(u[0]),
              a.sort(function (t, i) {
                return t.ti() - i.ti();
              }),
              i.forEach(function (t) {
                return t.oi(t.ti());
              }),
              this._i.R().alignLabels)
            ) {
              for (var o = 1; o < u.length; o++) {
                var l = u[o],
                  f = (v = u[o - 1]).Yt(h, !1);
                l.ti() > (_ = v.ai()) - f && l.oi(_ - f);
              }
              for (var c = 1; c < a.length; c++) {
                var v, _;
                (l = a[c]), (f = (v = a[c - 1]).Yt(h, !0));
                l.ti() < (_ = v.ai()) + f && l.oi(_ + f);
              }
            }
          }
        }),
        (t.prototype.U_ = function (t, i) {
          var n = this;
          if (null !== this.o_) {
            t.save();
            var s = this.o_,
              h = this.V_(),
              r = this.O_(),
              u = this.m_ ? "right" : "left";
            h.forEach(function (h) {
              if (h.fi()) {
                var a = h.dt(e(n._i));
                t.save(), a.H(t, r, n.f_, s.Ot, u, i), t.restore();
              }
            }),
              t.restore();
          }
        }),
        (t.prototype.H_ = function (t, i) {
          var n = this;
          if (null !== this.o_ && null !== this._i) {
            t.save();
            var s = this.o_,
              h = this.Di.M_().jt(),
              r = [],
              u = this.Di.z_(),
              a = h.Tf().nn(u, this._i);
            a.length && r.push(a);
            var o = this.O_(),
              l = this.m_ ? "right" : "left";
            r.forEach(function (h) {
              h.forEach(function (h) {
                t.save(), h.dt(e(n._i)).H(t, o, n.f_, s.Ot, l, i), t.restore();
              });
            }),
              t.restore();
          }
        }),
        (t.prototype.K_ = function (t) {
          this.g_.style.cursor = 1 === t ? "ns-resize" : "default";
        }),
        (t.prototype.Eu = function () {
          var t = this.F_();
          this.v_ < t && this.Di.M_().jt().Ce(), (this.v_ = t);
        }),
        (t.prototype.w_ = function (t) {
          this.c_.p(), (this.c_ = new Fn(t.S, t.A, t.D));
        }),
        t
      );
    })();
  function Pn(t, i, n, s, h) {
    t.$ && t.$(i, n, s, h);
  }
  function Rn(t, i, n, s, h) {
    t.H(i, n, s, h);
  }
  function zn(t, i) {
    return t.tn(i);
  }
  function Wn(t, i) {
    return void 0 !== t.Pe ? t.Pe(i) : [];
  }
  var In = (function () {
      function t(t, i) {
        var n = this;
        (this.o_ = new Mn(0, 0)),
          (this.X_ = null),
          (this.Z_ = null),
          (this.J_ = null),
          (this.G_ = !1),
          (this.Q_ = new p()),
          (this.td = 0),
          (this.nd = !1),
          (this.sd = null),
          (this.hd = !1),
          (this.rd = null),
          (this.ed = null),
          (this.__ = !1),
          (this.d_ = function () {
            n.__ || null === n.ud || n.gi().Rr();
          }),
          (this.b_ = function () {
            n.__ || null === n.ud || n.gi().Rr();
          }),
          (this.ad = t),
          (this.ud = i),
          this.ud.ro().u(this.od.bind(this), this, !0),
          (this.ld = document.createElement("td")),
          (this.ld.style.padding = "0"),
          (this.ld.style.position = "relative");
        var s = document.createElement("div");
        (s.style.width = "100%"),
          (s.style.height = "100%"),
          (s.style.position = "relative"),
          (s.style.overflow = "hidden"),
          (this.fd = document.createElement("td")),
          (this.fd.style.padding = "0"),
          (this.vd = document.createElement("td")),
          (this.vd.style.padding = "0"),
          this.ld.appendChild(s),
          (this.p_ = pn(s, new Mn(16, 16))),
          this.p_.subscribeCanvasConfigured(this.d_);
        var h = this.p_.canvas;
        (h.style.position = "absolute"),
          (h.style.zIndex = "1"),
          (h.style.left = "0"),
          (h.style.top = "0"),
          (this.y_ = pn(s, new Mn(16, 16))),
          this.y_.subscribeCanvasConfigured(this.b_);
        var r = this.y_.canvas;
        (r.style.position = "absolute"),
          (r.style.zIndex = "2"),
          (r.style.left = "0"),
          (r.style.top = "0"),
          (this._d = document.createElement("tr")),
          this._d.appendChild(this.fd),
          this._d.appendChild(this.ld),
          this._d.appendChild(this.vd),
          this.dd(),
          (this.A_ = new Dn(this.y_.canvas, this, {
            _v: function () {
              return null === n.sd && !n.ad.R().handleScroll.vertTouchDrag;
            },
            dv: function () {
              return null === n.sd && !n.ad.R().handleScroll.horzTouchDrag;
            },
          }));
      }
      return (
        (t.prototype.p = function () {
          null !== this.X_ && this.X_.p(),
            null !== this.Z_ && this.Z_.p(),
            this.y_.unsubscribeCanvasConfigured(this.b_),
            this.y_.destroy(),
            this.p_.unsubscribeCanvasConfigured(this.d_),
            this.p_.destroy(),
            null !== this.ud && this.ud.ro().M(this),
            this.A_.p();
        }),
        (t.prototype.z_ = function () {
          return e(this.ud);
        }),
        (t.prototype.wd = function (i) {
          null !== this.ud && this.ud.ro().M(this),
            (this.ud = i),
            null !== this.ud &&
              this.ud.ro().u(t.prototype.od.bind(this), this, !0),
            this.dd();
        }),
        (t.prototype.M_ = function () {
          return this.ad;
        }),
        (t.prototype.B_ = function () {
          return this._d;
        }),
        (t.prototype.dd = function () {
          if (null !== this.ud && (this.Md(), 0 !== this.gi()._t().length)) {
            if (null !== this.X_) {
              var t = this.ud.Ya();
              this.X_.Si(e(t));
            }
            if (null !== this.Z_) {
              var i = this.ud.$a();
              this.Z_.Si(e(i));
            }
          }
        }),
        (t.prototype.bd = function () {
          null !== this.X_ && this.X_.vt(), null !== this.Z_ && this.Z_.vt();
        }),
        (t.prototype.Ra = function () {
          return null !== this.ud ? this.ud.Ra() : 0;
        }),
        (t.prototype.za = function (t) {
          this.ud && this.ud.za(t);
        }),
        (t.prototype.ov = function (t) {
          if (this.ud) {
            this.md();
            var i = t.Yv,
              n = t.$v;
            this.gd(i, n);
          }
        }),
        (t.prototype.Tv = function (t) {
          this.md(), this.pd(), this.gd(t.Yv, t.$v);
        }),
        (t.prototype.lv = function (t) {
          if (this.ud) {
            this.md();
            var i = t.Yv,
              n = t.$v;
            this.gd(i, n);
            var s = this.$h(i, n);
            this.gi().yf(s && { kf: s.kf, yd: s.yd });
          }
        }),
        (t.prototype.kv = function (t) {
          if (null !== this.ud) {
            this.md();
            var i = t.Yv,
              n = t.$v;
            if (this.Q_.g()) {
              var s = this.gi().Tf().Mt();
              this.Q_.m(s, { x: i, y: n });
            }
          }
        }),
        (t.prototype.bv = function (t) {
          this.md(), this.kd(t), this.gd(t.Yv, t.$v);
        }),
        (t.prototype.yv = function (t) {
          null !== this.ud && (this.md(), (this.nd = !1), this.xd(t));
        }),
        (t.prototype.zv = function (t) {
          if (((this.nd = !0), null === this.sd)) {
            var i = { x: t.Yv, y: t.$v };
            this.Nd(i, i);
          }
        }),
        (t.prototype.Rv = function (t) {
          null !== this.ud && (this.md(), this.ud.jt().yf(null), this.Cd());
        }),
        (t.prototype.Sd = function () {
          return this.Q_;
        }),
        (t.prototype.Lv = function () {
          (this.td = 1), this.Td();
        }),
        (t.prototype.Ev = function (t, i) {
          if (this.ad.R().handleScale.pinch) {
            var n = 5 * (i - this.td);
            (this.td = i), this.gi().Ef(t.tt, n);
          }
        }),
        (t.prototype.Cv = function (t) {
          if (
            ((this.nd = !1),
            (this.hd = null !== this.sd),
            this.pd(),
            null !== this.sd)
          ) {
            var i = this.gi().Tf();
            (this.rd = { x: i.$t(), y: i.Kt() }),
              (this.sd = { x: t.Yv, y: t.$v });
          }
        }),
        (t.prototype.wv = function (t) {
          if (null !== this.ud) {
            var i = t.Yv,
              n = t.$v;
            if (null === this.sd) this.kd(t);
            else {
              this.hd = !1;
              var s = e(this.rd),
                h = s.x + (i - this.sd.x),
                r = s.y + (n - this.sd.y);
              this.gd(h, r);
            }
          }
        }),
        (t.prototype.gv = function (t) {
          0 === this.M_().R().trackingMode.exitMode && (this.hd = !0),
            this.Dd(),
            this.xd(t);
        }),
        (t.prototype.$h = function (t, i) {
          var n = this.ud;
          if (null === n) return null;
          for (var s = 0, h = n.oa(); s < h.length; s++) {
            var r = h[s],
              e = this.Ad(r.tn(n), t, i);
            if (null !== e) return { kf: r, i_: e.i_, yd: e.yd };
          }
          return null;
        }),
        (t.prototype.Bd = function (t, i) {
          e("left" === i ? this.X_ : this.Z_).P_(new Mn(t, this.o_.Ft));
        }),
        (t.prototype.Ld = function () {
          return this.o_;
        }),
        (t.prototype.P_ = function (t) {
          if (t.Ot < 0 || t.Ft < 0)
            throw new Error(
              "Try to set invalid size to PaneWidget " + JSON.stringify(t)
            );
          this.o_.br(t) ||
            ((this.o_ = t),
            (this.__ = !0),
            this.p_.resizeCanvas({ width: t.Ot, height: t.Ft }),
            this.y_.resizeCanvas({ width: t.Ot, height: t.Ft }),
            (this.__ = !1),
            (this.ld.style.width = t.Ot + "px"),
            (this.ld.style.height = t.Ft + "px"));
        }),
        (t.prototype.Ed = function () {
          var t = e(this.ud);
          t.Ha(t.Ya()), t.Ha(t.$a());
          for (var i = 0, n = t.Ge(); i < n.length; i++) {
            var s = n[i];
            if (t.lh(s)) {
              var h = s.Ct();
              null !== h && t.Ha(h), s.hn();
            }
          }
        }),
        (t.prototype.Y_ = function () {
          return this.p_.canvas;
        }),
        (t.prototype.W_ = function (t) {
          if (0 !== t && null !== this.ud) {
            if (
              (t > 1 && this.Ed(),
              null !== this.X_ && this.X_.W_(t),
              null !== this.Z_ && this.Z_.W_(t),
              1 !== t)
            ) {
              var i = mn(this.p_.canvas);
              i.save(),
                this.j_(i, this.p_.pixelRatio),
                this.ud &&
                  (this.Od(i, this.p_.pixelRatio),
                  this.Fd(i, this.p_.pixelRatio),
                  this.Vd(i, this.p_.pixelRatio, zn)),
                i.restore();
            }
            var n = mn(this.y_.canvas);
            n.clearRect(
              0,
              0,
              Math.ceil(this.o_.Ot * this.y_.pixelRatio),
              Math.ceil(this.o_.Ft * this.y_.pixelRatio)
            ),
              this.Vd(n, this.p_.pixelRatio, Wn),
              this.Pd(n, this.y_.pixelRatio);
          }
        }),
        (t.prototype.Rd = function () {
          return this.X_;
        }),
        (t.prototype.zd = function () {
          return this.Z_;
        }),
        (t.prototype.od = function () {
          null !== this.ud && this.ud.ro().M(this), (this.ud = null);
        }),
        (t.prototype.j_ = function (t, i) {
          var n = this;
          j(t, i, function () {
            var i = n.gi(),
              s = i.Zf(),
              h = i.Xf();
            s === h
              ? q(t, 0, 0, n.o_.Ot, n.o_.Ft, h)
              : U(t, 0, 0, n.o_.Ot, n.o_.Ft, s, h);
          });
        }),
        (t.prototype.Od = function (t, i) {
          var n = e(this.ud),
            s = n.eo().ou().dt(n.Yt(), n.Ht());
          null !== s && (t.save(), s.H(t, i, !1), t.restore());
        }),
        (t.prototype.Fd = function (t, i) {
          var n = this.gi().Sf();
          this.Wd(t, i, zn, Pn, n), this.Wd(t, i, zn, Rn, n);
        }),
        (t.prototype.Pd = function (t, i) {
          this.Wd(t, i, zn, Rn, this.gi().Tf());
        }),
        (t.prototype.Vd = function (t, i, n) {
          for (var s = e(this.ud).oa(), h = 0, r = s; h < r.length; h++) {
            var u = r[h];
            this.Wd(t, i, n, Pn, u);
          }
          for (var a = 0, o = s; a < o.length; a++) {
            u = o[a];
            this.Wd(t, i, n, Rn, u);
          }
        }),
        (t.prototype.Wd = function (t, i, n, s, h) {
          for (
            var r = e(this.ud),
              u = n(h, r),
              a = r.Yt(),
              o = r.Ht(),
              l = r.jt().pf(),
              f = null !== l && l.kf === h,
              c = null !== l && f && void 0 !== l.yd ? l.yd.Kh : void 0,
              v = 0,
              _ = u;
            v < _.length;
            v++
          ) {
            var d = _[v].dt(a, o);
            null !== d && (t.save(), s(d, t, i, f, c), t.restore());
          }
        }),
        (t.prototype.Ad = function (t, i, n) {
          for (var s = 0, h = t; s < h.length; s++) {
            var r = h[s],
              e = r.dt(this.o_.Ft, this.o_.Ot);
            if (null !== e && e.$h) {
              var u = e.$h(i, n);
              if (null !== u) return { i_: r, yd: u };
            }
          }
          return null;
        }),
        (t.prototype.Md = function () {
          if (null !== this.ud) {
            var t = this.ad,
              i = this.ud.Ya().R().visible,
              n = this.ud.$a().R().visible;
            i ||
              null === this.X_ ||
              (this.fd.removeChild(this.X_.B_()),
              this.X_.p(),
              (this.X_ = null)),
              n ||
                null === this.Z_ ||
                (this.vd.removeChild(this.Z_.B_()),
                this.Z_.p(),
                (this.Z_ = null));
            var s = t.jt().qf();
            i &&
              null === this.X_ &&
              ((this.X_ = new Vn(this, t.R().layout, s, "left")),
              this.fd.appendChild(this.X_.B_())),
              n &&
                null === this.Z_ &&
                ((this.Z_ = new Vn(this, t.R().layout, s, "right")),
                this.vd.appendChild(this.Z_.B_()));
          }
        }),
        (t.prototype.Id = function (t) {
          return (t.Gv && this.nd) || null !== this.sd;
        }),
        (t.prototype.jd = function (t) {
          return Math.max(0, Math.min(t, this.o_.Ot - 1));
        }),
        (t.prototype.qd = function (t) {
          return Math.max(0, Math.min(t, this.o_.Ft - 1));
        }),
        (t.prototype.gd = function (t, i) {
          this.gi().Wf(this.jd(t), this.qd(i), e(this.ud));
        }),
        (t.prototype.Cd = function () {
          this.gi().If();
        }),
        (t.prototype.Dd = function () {
          this.hd && ((this.sd = null), this.Cd());
        }),
        (t.prototype.Nd = function (t, i) {
          (this.sd = t), (this.hd = !1), this.gd(i.x, i.y);
          var n = this.gi().Tf();
          this.rd = { x: n.$t(), y: n.Kt() };
        }),
        (t.prototype.gi = function () {
          return this.ad.jt();
        }),
        (t.prototype.Ud = function () {
          var t = this.gi(),
            i = this.z_(),
            n = i.ji();
          t.Qa(i, n), t.Pf(), (this.J_ = null), (this.G_ = !1);
        }),
        (t.prototype.xd = function (t) {
          var i = this;
          if (this.G_) {
            var n = performance.now();
            if (
              (null !== this.ed && this.ed.Nh(t.Yv, n),
              null === this.ed || this.ed.cc(n))
            )
              this.Ud();
            else {
              var s = this.gi(),
                h = s.bt(),
                r = this.ed,
                e = function () {
                  if (!r._c()) {
                    var t = performance.now(),
                      n = r.cc(t);
                    if (!r._c()) {
                      var u = h.xl();
                      s.Vf(r.fc(t)), u === h.xl() && ((n = !0), (i.ed = null));
                    }
                    n ? i.Ud() : requestAnimationFrame(e);
                  }
                };
              requestAnimationFrame(e);
            }
          }
        }),
        (t.prototype.md = function () {
          this.sd = null;
        }),
        (t.prototype.pd = function () {
          if (this.ud) {
            if (
              (this.Td(),
              document.activeElement !== document.body &&
                document.activeElement !== document.documentElement)
            )
              e(document.activeElement).blur();
            else {
              var t = document.getSelection();
              null !== t && t.removeAllRanges();
            }
            !this.ud.ji().wi() && this.gi().bt().wi();
          }
        }),
        (t.prototype.kd = function (t) {
          if (null !== this.ud) {
            var i = this.gi();
            if (!i.bt().wi()) {
              var n = this.ad.R(),
                s = n.handleScroll,
                h = n.kineticScroll;
              if (
                (s.pressedMouseMove && !t.Gv) ||
                ((s.horzTouchDrag || s.vertTouchDrag) && t.Gv)
              ) {
                var r = this.ud.ji(),
                  e = performance.now();
                null !== this.J_ ||
                  this.Id(t) ||
                  (this.J_ = { x: t.Wv, y: t.Iv, So: e, Yv: t.Yv, $v: t.$v }),
                  null !== this.ed && this.ed.lc(t.Yv, e),
                  null === this.J_ ||
                    this.G_ ||
                    (this.J_.x === t.Wv && this.J_.y === t.Iv) ||
                    (null === this.ed &&
                      ((t.Gv && h.touch) || (!t.Gv && h.mouse)) &&
                      ((this.ed = new xn(0.2, 7, 0.997, 15)),
                      this.ed.lc(this.J_.Yv, this.J_.So),
                      this.ed.lc(t.Yv, e)),
                    r.wi() || i.Ja(this.ud, r, t.$v),
                    i.Ff(t.Yv),
                    (this.G_ = !0)),
                  this.G_ && (r.wi() || i.Ga(this.ud, r, t.$v), i.Vf(t.Yv));
              }
            }
          }
        }),
        (t.prototype.Td = function () {
          var t = performance.now(),
            i = null === this.ed || this.ed.cc(t);
          null !== this.ed && (i || this.Ud()),
            null !== this.ed && (this.ed.dc(), (this.ed = null));
        }),
        t
      );
    })(),
    jn = (function () {
      function t(t, i, n, s, h) {
        var r = this;
        (this.ft = !0),
          (this.o_ = new Mn(0, 0)),
          (this.d_ = function () {
            return r.W_(3);
          }),
          (this.m_ = "left" === t),
          (this.cf = n.qf),
          (this.zi = i),
          (this.Hd = s),
          (this.Yd = h),
          (this.g_ = document.createElement("div")),
          (this.g_.style.width = "25px"),
          (this.g_.style.height = "100%"),
          (this.g_.style.overflow = "hidden"),
          (this.p_ = pn(this.g_, new Mn(16, 16))),
          this.p_.subscribeCanvasConfigured(this.d_);
      }
      return (
        (t.prototype.p = function () {
          this.p_.unsubscribeCanvasConfigured(this.d_), this.p_.destroy();
        }),
        (t.prototype.B_ = function () {
          return this.g_;
        }),
        (t.prototype.Ld = function () {
          return this.o_;
        }),
        (t.prototype.P_ = function (t) {
          if (t.Ot < 0 || t.Ft < 0)
            throw new Error(
              "Try to set invalid size to PriceAxisStub " + JSON.stringify(t)
            );
          this.o_.br(t) ||
            ((this.o_ = t),
            this.p_.resizeCanvas({ width: t.Ot, height: t.Ft }),
            (this.g_.style.width = "".concat(t.Ot, "px")),
            (this.g_.style.minWidth = "".concat(t.Ot, "px")),
            (this.g_.style.height = "".concat(t.Ft, "px")),
            (this.ft = !0));
        }),
        (t.prototype.W_ = function (t) {
          if ((!(t < 3) || this.ft) && 0 !== this.o_.Ot && 0 !== this.o_.Ft) {
            this.ft = !1;
            var i = mn(this.p_.canvas);
            this.j_(i, this.p_.pixelRatio), this.Ws(i, this.p_.pixelRatio);
          }
        }),
        (t.prototype.Y_ = function () {
          return this.p_.canvas;
        }),
        (t.prototype.Ws = function (t, i) {
          if (this.Hd()) {
            var n = this.o_.Ot;
            t.save(), (t.fillStyle = this.zi.timeScale.borderColor);
            var s = Math.floor(this.cf.R().N * i),
              h = this.m_ ? Math.round(n * i) - s : 0;
            t.fillRect(h, 0, s, s), t.restore();
          }
        }),
        (t.prototype.j_ = function (t, i) {
          var n = this;
          j(t, i, function () {
            q(t, 0, 0, n.o_.Ot, n.o_.Ft, n.Yd());
          });
        }),
        t
      );
    })();
  function qn(t, i) {
    return t.Po > i.Po ? t : i;
  }
  var Un = (function () {
      function t(t) {
        var i = this;
        (this.$d = null),
          (this.Kd = null),
          (this.k = null),
          (this.Xd = !1),
          (this.o_ = new Mn(0, 0)),
          (this.Zd = new p()),
          (this.f_ = new zt(5)),
          (this.__ = !1),
          (this.d_ = function () {
            i.__ || i.ad.jt().Rr();
          }),
          (this.b_ = function () {
            i.__ || i.ad.jt().Rr();
          }),
          (this.ad = t),
          (this.zi = t.R().layout),
          (this.Jd = document.createElement("tr")),
          (this.Gd = document.createElement("td")),
          (this.Gd.style.padding = "0"),
          (this.Qd = document.createElement("td")),
          (this.Qd.style.padding = "0"),
          (this.g_ = document.createElement("td")),
          (this.g_.style.height = "25px"),
          (this.g_.style.padding = "0"),
          (this.tw = document.createElement("div")),
          (this.tw.style.width = "100%"),
          (this.tw.style.height = "100%"),
          (this.tw.style.position = "relative"),
          (this.tw.style.overflow = "hidden"),
          this.g_.appendChild(this.tw),
          (this.p_ = pn(this.tw, new Mn(16, 16))),
          this.p_.subscribeCanvasConfigured(this.d_);
        var n = this.p_.canvas;
        (n.style.position = "absolute"),
          (n.style.zIndex = "1"),
          (n.style.left = "0"),
          (n.style.top = "0"),
          (this.y_ = pn(this.tw, new Mn(16, 16))),
          this.y_.subscribeCanvasConfigured(this.b_);
        var s = this.y_.canvas;
        (s.style.position = "absolute"),
          (s.style.zIndex = "2"),
          (s.style.left = "0"),
          (s.style.top = "0"),
          this.Jd.appendChild(this.Gd),
          this.Jd.appendChild(this.g_),
          this.Jd.appendChild(this.Qd),
          this.iw(),
          this.ad.jt().Pa().u(this.iw.bind(this), this),
          (this.A_ = new Dn(this.y_.canvas, this, {
            _v: function () {
              return !0;
            },
            dv: function () {
              return !1;
            },
          }));
      }
      return (
        (t.prototype.p = function () {
          this.A_.p(),
            null !== this.$d && this.$d.p(),
            null !== this.Kd && this.Kd.p(),
            this.y_.unsubscribeCanvasConfigured(this.b_),
            this.y_.destroy(),
            this.p_.unsubscribeCanvasConfigured(this.d_),
            this.p_.destroy();
        }),
        (t.prototype.B_ = function () {
          return this.Jd;
        }),
        (t.prototype.nw = function () {
          return this.$d;
        }),
        (t.prototype.sw = function () {
          return this.Kd;
        }),
        (t.prototype.Tv = function (t) {
          if (!this.Xd) {
            this.Xd = !0;
            var i = this.ad.jt();
            !i.bt().wi() &&
              this.ad.R().handleScale.axisPressedMouseMove.time &&
              i.Lf(t.Yv);
          }
        }),
        (t.prototype.Cv = function (t) {
          this.Tv(t);
        }),
        (t.prototype.Dv = function () {
          var t = this.ad.jt();
          !t.bt().wi() &&
            this.Xd &&
            ((this.Xd = !1),
            this.ad.R().handleScale.axisPressedMouseMove.time && t.zf());
        }),
        (t.prototype.bv = function (t) {
          var i = this.ad.jt();
          !i.bt().wi() &&
            this.ad.R().handleScale.axisPressedMouseMove.time &&
            i.Rf(t.Yv);
        }),
        (t.prototype.wv = function (t) {
          this.bv(t);
        }),
        (t.prototype.yv = function () {
          this.Xd = !1;
          var t = this.ad.jt();
          (t.bt().wi() && !this.ad.R().handleScale.axisPressedMouseMove.time) ||
            t.zf();
        }),
        (t.prototype.gv = function () {
          this.yv();
        }),
        (t.prototype.nv = function () {
          this.ad.R().handleScale.axisDoubleClickReset && this.ad.jt().gn();
        }),
        (t.prototype.Gc = function () {
          this.nv();
        }),
        (t.prototype.ov = function () {
          this.ad.jt().R().handleScale.axisPressedMouseMove.time && this.K_(1);
        }),
        (t.prototype.Rv = function () {
          this.K_(0);
        }),
        (t.prototype.Ld = function () {
          return this.o_;
        }),
        (t.prototype.hw = function () {
          return this.Zd;
        }),
        (t.prototype.rw = function (t, i, n) {
          (this.o_ && this.o_.br(t)) ||
            ((this.o_ = t),
            (this.__ = !0),
            this.p_.resizeCanvas({ width: t.Ot, height: t.Ft }),
            this.y_.resizeCanvas({ width: t.Ot, height: t.Ft }),
            (this.__ = !1),
            (this.g_.style.width = t.Ot + "px"),
            (this.g_.style.height = t.Ft + "px"),
            this.Zd.m(t)),
            null !== this.$d && this.$d.P_(new Mn(i, t.Ft)),
            null !== this.Kd && this.Kd.P_(new Mn(n, t.Ft));
        }),
        (t.prototype.ew = function () {
          var t = this.uw();
          return Math.ceil(t.N + t.C + t.S + t.F + t.B);
        }),
        (t.prototype.vt = function () {
          this.ad.jt().bt().au();
        }),
        (t.prototype.Y_ = function () {
          return this.p_.canvas;
        }),
        (t.prototype.W_ = function (t) {
          if (0 !== t) {
            if (1 !== t) {
              var i = mn(this.p_.canvas);
              this.j_(i, this.p_.pixelRatio),
                this.Ws(i, this.p_.pixelRatio),
                this.q_(i, this.p_.pixelRatio),
                null !== this.$d && this.$d.W_(t),
                null !== this.Kd && this.Kd.W_(t);
            }
            var n = mn(this.y_.canvas),
              s = this.y_.pixelRatio;
            n.clearRect(
              0,
              0,
              Math.ceil(this.o_.Ot * s),
              Math.ceil(this.o_.Ft * s)
            ),
              this.aw([this.ad.jt().Tf()], n, s);
          }
        }),
        (t.prototype.j_ = function (t, i) {
          var n = this;
          j(t, i, function () {
            q(t, 0, 0, n.o_.Ot, n.o_.Ft, n.ad.jt().Xf());
          });
        }),
        (t.prototype.Ws = function (t, i) {
          if (this.ad.R().timeScale.borderVisible) {
            t.save(), (t.fillStyle = this.ow());
            var n = Math.max(1, Math.floor(this.uw().N * i));
            t.fillRect(0, 0, Math.ceil(this.o_.Ot * i), n), t.restore();
          }
        }),
        (t.prototype.q_ = function (t, i) {
          var n = this,
            s = this.ad.jt().bt().au();
          if (s && 0 !== s.length) {
            var h = s.reduce(qn, s[0]).Po;
            h > 30 && h < 50 && (h = 30), t.save(), (t.strokeStyle = this.ow());
            var r = this.uw(),
              e = r.N + r.C + r.F + r.S - r.V;
            (t.textAlign = "center"), (t.fillStyle = this.ow());
            var u = Math.floor(this.uw().N * i),
              a = Math.max(1, Math.floor(i)),
              o = Math.floor(0.5 * i);
            if (this.ad.jt().bt().R().borderVisible) {
              t.beginPath();
              for (var l = Math.round(r.C * i), f = s.length; f--; ) {
                var c = Math.round(s[f].su * i);
                t.rect(c - o, u, a, l);
              }
              t.fill();
            }
            (t.fillStyle = this.j()),
              j(t, i, function () {
                t.font = n.lw();
                for (var i = 0, r = s; i < r.length; i++) {
                  if ((l = r[i]).Po < h) {
                    var u = l.Sl ? n.fw(t, l.su, l.yu) : l.su;
                    t.fillText(l.yu, u, e);
                  }
                }
                t.font = n.cw();
                for (var a = 0, o = s; a < o.length; a++) {
                  var l;
                  if ((l = o[a]).Po >= h) {
                    u = l.Sl ? n.fw(t, l.su, l.yu) : l.su;
                    t.fillText(l.yu, u, e);
                  }
                }
              }),
              t.restore();
          }
        }),
        (t.prototype.fw = function (t, i, n) {
          var s = this.f_.Qt(t, n),
            h = s / 2,
            r = Math.floor(i - h) + 0.5;
          return (
            r < 0
              ? (i += Math.abs(0 - r))
              : r + s > this.o_.Ot && (i -= Math.abs(this.o_.Ot - (r + s))),
            i
          );
        }),
        (t.prototype.aw = function (t, i, n) {
          for (var s = this.uw(), h = 0, r = t; h < r.length; h++)
            for (var e = 0, u = r[h].Ti(); e < u.length; e++) {
              var a = u[e];
              i.save(), a.dt().H(i, s, n), i.restore();
            }
        }),
        (t.prototype.ow = function () {
          return this.ad.R().timeScale.borderColor;
        }),
        (t.prototype.j = function () {
          return this.zi.textColor;
        }),
        (t.prototype.W = function () {
          return this.zi.fontSize;
        }),
        (t.prototype.lw = function () {
          return B(this.W(), this.zi.fontFamily);
        }),
        (t.prototype.cw = function () {
          return B(this.W(), this.zi.fontFamily, "bold");
        }),
        (t.prototype.uw = function () {
          null === this.k &&
            (this.k = {
              N: 1,
              V: NaN,
              F: NaN,
              B: NaN,
              mi: NaN,
              C: 3,
              S: NaN,
              T: "",
              bi: new zt(),
            });
          var t = this.k,
            i = this.lw();
          if (t.T !== i) {
            var n = this.W();
            (t.S = n),
              (t.T = i),
              (t.F = Math.ceil(n / 2.5)),
              (t.B = t.F),
              (t.mi = Math.ceil(n / 2)),
              (t.V = Math.round(this.W() / 5)),
              t.bi.ih();
          }
          return this.k;
        }),
        (t.prototype.K_ = function (t) {
          this.g_.style.cursor = 1 === t ? "ew-resize" : "default";
        }),
        (t.prototype.iw = function () {
          var t = this.ad.jt(),
            i = t.R();
          i.leftPriceScale.visible ||
            null === this.$d ||
            (this.Gd.removeChild(this.$d.B_()), this.$d.p(), (this.$d = null)),
            i.rightPriceScale.visible ||
              null === this.Kd ||
              (this.Qd.removeChild(this.Kd.B_()),
              this.Kd.p(),
              (this.Kd = null));
          var n = { qf: this.ad.jt().qf() },
            s = function () {
              return i.leftPriceScale.borderVisible && t.bt().R().borderVisible;
            },
            h = function () {
              return t.Xf();
            };
          i.leftPriceScale.visible &&
            null === this.$d &&
            ((this.$d = new jn("left", i, n, s, h)),
            this.Gd.appendChild(this.$d.B_())),
            i.rightPriceScale.visible &&
              null === this.Kd &&
              ((this.Kd = new jn("right", i, n, s, h)),
              this.Qd.appendChild(this.Kd.B_()));
        }),
        t
      );
    })(),
    Hn = (function () {
      function t(t, i) {
        var n;
        (this._w = []),
          (this.dw = 0),
          (this.Nu = 0),
          (this.hh = 0),
          (this.ww = 0),
          (this.Mw = 0),
          (this.bw = null),
          (this.mw = !1),
          (this.Q_ = new p()),
          (this.af = new p()),
          (this.zi = i),
          (this.Jd = document.createElement("div")),
          this.Jd.classList.add("tv-lightweight-charts"),
          (this.Jd.style.overflow = "hidden"),
          (this.Jd.style.width = "100%"),
          (this.Jd.style.height = "100%"),
          ((n = this.Jd).style.userSelect = "none"),
          (n.style.webkitUserSelect = "none"),
          (n.style.msUserSelect = "none"),
          (n.style.MozUserSelect = "none"),
          (n.style.webkitTapHighlightColor = "transparent"),
          (this.gw = document.createElement("table")),
          this.gw.setAttribute("cellspacing", "0"),
          this.Jd.appendChild(this.gw),
          (this.pw = this.yw.bind(this)),
          this.Jd.addEventListener("wheel", this.pw, { passive: !1 }),
          (this.gi = new fn(this.ff.bind(this), this.zi)),
          this.jt().Df().u(this.kw.bind(this), this),
          (this.xw = new Un(this)),
          this.gw.appendChild(this.xw.B_());
        var s = this.zi.width,
          h = this.zi.height;
        if (0 === s || 0 === h) {
          var r = t.getBoundingClientRect();
          0 === s && ((s = Math.floor(r.width)), (s -= s % 2)),
            0 === h && ((h = Math.floor(r.height)), (h -= h % 2));
        }
        this.Nw(s, h),
          this.Cw(),
          t.appendChild(this.Jd),
          this.Sw(),
          this.gi.bt().Pl().u(this.gi.Ce.bind(this.gi), this),
          this.gi.Pa().u(this.gi.Ce.bind(this.gi), this);
      }
      return (
        (t.prototype.jt = function () {
          return this.gi;
        }),
        (t.prototype.R = function () {
          return this.zi;
        }),
        (t.prototype.Tw = function () {
          return this._w;
        }),
        (t.prototype.Dw = function () {
          return this.xw;
        }),
        (t.prototype.p = function () {
          this.Jd.removeEventListener("wheel", this.pw),
            0 !== this.dw && window.cancelAnimationFrame(this.dw),
            this.gi.Df().M(this),
            this.gi.bt().Pl().M(this),
            this.gi.Pa().M(this),
            this.gi.p();
          for (var t = 0, i = this._w; t < i.length; t++) {
            var n = i[t];
            this.gw.removeChild(n.B_()), n.Sd().M(this), n.p();
          }
          (this._w = []),
            e(this.xw).p(),
            null !== this.Jd.parentElement &&
              this.Jd.parentElement.removeChild(this.Jd),
            this.af.p(),
            this.Q_.p();
        }),
        (t.prototype.Nw = function (t, i, n) {
          if ((void 0 === n && (n = !1), this.Nu !== i || this.hh !== t)) {
            (this.Nu = i), (this.hh = t);
            var s = i + "px",
              h = t + "px";
            (e(this.Jd).style.height = s),
              (e(this.Jd).style.width = h),
              (this.gw.style.height = s),
              (this.gw.style.width = h),
              n ? this.Aw(new it(3)) : this.gi.Ce();
          }
        }),
        (t.prototype.W_ = function (t) {
          void 0 === t && (t = new it(3));
          for (var i = 0; i < this._w.length; i++) this._w[i].W_(t.wn(i).vn);
          this.zi.timeScale.visible && this.xw.W_(t.dn());
        }),
        (t.prototype.Pr = function (t) {
          this.gi.Pr(t), this.Sw();
          var i = t.width || this.hh,
            n = t.height || this.Nu;
          this.Nw(i, n);
        }),
        (t.prototype.Sd = function () {
          return this.Q_;
        }),
        (t.prototype.Df = function () {
          return this.af;
        }),
        (t.prototype.Bw = function () {
          var t = this;
          null !== this.bw && (this.Aw(this.bw), (this.bw = null));
          var i = this._w[0],
            n = gn(document, new Mn(this.hh, this.Nu)),
            s = mn(n),
            h = bn(n);
          return (
            j(s, h, function () {
              var n = 0,
                h = 0,
                r = function (i) {
                  for (var r = 0; r < t._w.length; r++) {
                    var u = t._w[r],
                      a = u.Ld().Ft,
                      o = e("left" === i ? u.Rd() : u.zd()),
                      l = o.Y_();
                    s.drawImage(l, n, h, o.R_(), a), (h += a);
                  }
                };
              t.Lw() && (r("left"), (n = e(i.Rd()).R_())), (h = 0);
              for (var u = 0; u < t._w.length; u++) {
                var a = t._w[u],
                  o = a.Ld(),
                  l = a.Y_();
                s.drawImage(l, n, h, o.Ot, o.Ft), (h += o.Ft);
              }
              (n += i.Ld().Ot), t.Ew() && ((h = 0), r("right"));
              var f = function (i) {
                var r = e("left" === i ? t.xw.nw() : t.xw.sw()),
                  u = r.Ld(),
                  a = r.Y_();
                s.drawImage(a, n, h, u.Ot, u.Ft);
              };
              if (t.zi.timeScale.visible) {
                (n = 0), t.Lw() && (f("left"), (n = e(i.Rd()).R_()));
                var c = t.xw.Ld();
                l = t.xw.Y_();
                s.drawImage(l, n, h, c.Ot, c.Ft),
                  t.Ew() && ((n += i.Ld().Ot), f("right"), s.restore());
              }
            }),
            n
          );
        }),
        (t.prototype.Ow = function (t) {
          return "none" === t
            ? 0
            : ("left" !== t || this.Lw()) && ("right" !== t || this.Ew())
            ? 0 === this._w.length
              ? 0
              : e("left" === t ? this._w[0].Rd() : this._w[0].zd()).R_()
            : 0;
        }),
        (t.prototype.Fw = function () {
          for (var t = 0, i = 0, n = 0, s = 0, h = this._w; s < h.length; s++) {
            var r = h[s];
            this.Lw() && (i = Math.max(i, e(r.Rd()).F_())),
              this.Ew() && (n = Math.max(n, e(r.zd()).F_())),
              (t += r.Ra());
          }
          var u = this.hh,
            a = this.Nu,
            o = Math.max(u - i - n, 0),
            l = this.zi.timeScale.visible,
            f = l ? this.xw.ew() : 0;
          f % 2 && (f += 1);
          for (
            var c = 0 + f, v = a < c ? 0 : a - c, _ = v / t, d = 0, w = 0;
            w < this._w.length;
            ++w
          ) {
            (r = this._w[w]).wd(this.gi.Cf()[w]);
            var M,
              b = 0;
            (b = w === this._w.length - 1 ? v - d : Math.round(r.Ra() * _)),
              (d += M = Math.max(b, 2)),
              r.P_(new Mn(o, M)),
              this.Lw() && r.Bd(i, "left"),
              this.Ew() && r.Bd(n, "right"),
              r.z_() && this.gi.Af(r.z_(), M);
          }
          this.xw.rw(new Mn(l ? o : 0, f), l ? i : 0, l ? n : 0),
            this.gi.Wa(o),
            this.ww !== i && (this.ww = i),
            this.Mw !== n && (this.Mw = n);
        }),
        (t.prototype.yw = function (t) {
          var i = t.deltaX / 100,
            n = -t.deltaY / 100;
          if (
            (0 !== i && this.zi.handleScroll.mouseWheel) ||
            (0 !== n && this.zi.handleScale.mouseWheel)
          ) {
            switch ((t.cancelable && t.preventDefault(), t.deltaMode)) {
              case t.DOM_DELTA_PAGE:
                (i *= 120), (n *= 120);
                break;
              case t.DOM_DELTA_LINE:
                (i *= 32), (n *= 32);
            }
            if (0 !== n && this.zi.handleScale.mouseWheel) {
              var s = Math.sign(n) * Math.min(1, Math.abs(n)),
                h = t.clientX - this.Jd.getBoundingClientRect().left;
              this.jt().Ef(h, s);
            }
            0 !== i && this.zi.handleScroll.mouseWheel && this.jt().Of(-80 * i);
          }
        }),
        (t.prototype.Aw = function (t) {
          var i,
            n = t.dn();
          3 === n && this.Vw(),
            (3 !== n && 2 !== n) ||
              (this.Pw(t),
              this.Rw(t),
              this.xw.vt(),
              this._w.forEach(function (t) {
                t.bd();
              }),
              3 ===
                (null === (i = this.bw) || void 0 === i ? void 0 : i.dn()) &&
                (this.bw.xn(t),
                this.Vw(),
                this.Pw(this.bw),
                this.Rw(this.bw),
                (t = this.bw),
                (this.bw = null))),
            this.W_(t);
        }),
        (t.prototype.Rw = function (t) {
          for (var i = 0, n = t.kn(); i < n.length; i++) {
            var s = n[i];
            this.Nn(s);
          }
        }),
        (t.prototype.Pw = function (t) {
          for (var i = this.gi.Cf(), n = 0; n < i.length; n++)
            t.wn(n)._n && i[n].so();
        }),
        (t.prototype.Nn = function (t) {
          var i = this.gi.bt();
          switch (t.bn) {
            case 0:
              i.zl();
              break;
            case 1:
              i.Wl(t.St);
              break;
            case 2:
              i.pn(t.St);
              break;
            case 3:
              i.yn(t.St);
              break;
            case 4:
              i.Tl();
          }
        }),
        (t.prototype.ff = function (t) {
          var i = this;
          null !== this.bw ? this.bw.xn(t) : (this.bw = t),
            this.mw ||
              ((this.mw = !0),
              (this.dw = window.requestAnimationFrame(function () {
                if (((i.mw = !1), (i.dw = 0), null !== i.bw)) {
                  var t = i.bw;
                  (i.bw = null), i.Aw(t);
                }
              })));
        }),
        (t.prototype.Vw = function () {
          this.Cw();
        }),
        (t.prototype.Cw = function () {
          for (
            var t = this.gi.Cf(), i = t.length, n = this._w.length, s = i;
            s < n;
            s++
          ) {
            var h = r(this._w.pop());
            this.gw.removeChild(h.B_()), h.Sd().M(this), h.p();
          }
          for (s = n; s < i; s++) {
            (h = new In(this, t[s])).Sd().u(this.zw.bind(this), this),
              this._w.push(h),
              this.gw.insertBefore(h.B_(), this.xw.B_());
          }
          for (s = 0; s < i; s++) {
            var e = t[s];
            (h = this._w[s]).z_() !== e ? h.wd(e) : h.dd();
          }
          this.Sw(), this.Fw();
        }),
        (t.prototype.Ww = function (t, i) {
          var n,
            s = new Map();
          null !== t &&
            this.gi._t().forEach(function (i) {
              var n = i.er(t);
              null !== n && s.set(i, n);
            });
          if (null !== t) {
            var h = this.gi.bt().pi(t);
            null !== h && (n = h);
          }
          var r = this.jt().pf(),
            e = null !== r && r.kf instanceof pi ? r.kf : void 0,
            u = null !== r && void 0 !== r.yd ? r.yd.Zh : void 0;
          return { rt: n, Iw: i || void 0, jw: e, qw: s, Uw: u };
        }),
        (t.prototype.zw = function (t, i) {
          var n = this;
          this.Q_.m(function () {
            return n.Ww(t, i);
          });
        }),
        (t.prototype.kw = function (t, i) {
          var n = this;
          this.af.m(function () {
            return n.Ww(t, i);
          });
        }),
        (t.prototype.Sw = function () {
          var t = this.zi.timeScale.visible ? "" : "none";
          this.xw.B_().style.display = t;
        }),
        (t.prototype.Lw = function () {
          return this._w[0].z_().Ya().R().visible;
        }),
        (t.prototype.Ew = function () {
          return this._w[0].z_().$a().R().visible;
        }),
        t
      );
    })();
  function Yn(t, i, n) {
    var s = n.value;
    return { vs: i, rt: t, St: [s, s, s, s] };
  }
  function $n(t, i, n) {
    var s = n.value,
      h = { vs: i, rt: t, St: [s, s, s, s] };
    return "color" in n && void 0 !== n.color && (h.A = n.color), h;
  }
  function Kn(t) {
    return void 0 !== t.St;
  }
  function Xn(t) {
    return function (i, n, s) {
      return void 0 === (h = s).open && void 0 === h.value
        ? { rt: i, vs: n }
        : t(i, n, s);
      var h;
    };
  }
  var Zn = {
    Candlestick: Xn(function (t, i, n) {
      var s = { vs: i, rt: t, St: [n.open, n.high, n.low, n.close] };
      return (
        "color" in n && void 0 !== n.color && (s.A = n.color),
        "borderColor" in n &&
          void 0 !== n.borderColor &&
          (s.Tt = n.borderColor),
        "wickColor" in n && void 0 !== n.wickColor && (s.qs = n.wickColor),
        s
      );
    }),
    Bar: Xn(function (t, i, n) {
      var s = { vs: i, rt: t, St: [n.open, n.high, n.low, n.close] };
      return "color" in n && void 0 !== n.color && (s.A = n.color), s;
    }),
    Area: Xn(Yn),
    Baseline: Xn(Yn),
    Histogram: Xn($n),
    Line: Xn($n),
  };
  function Jn(t) {
    return Zn[t];
  }
  function Gn(t) {
    return 60 * t * 60 * 1e3;
  }
  function Qn(t) {
    return 60 * t * 1e3;
  }
  var ts,
    is = [
      { Hw: ((ts = 1), 1e3 * ts), Po: 10 },
      { Hw: Qn(1), Po: 20 },
      { Hw: Qn(5), Po: 21 },
      { Hw: Qn(30), Po: 22 },
      { Hw: Gn(1), Po: 30 },
      { Hw: Gn(3), Po: 31 },
      { Hw: Gn(6), Po: 32 },
      { Hw: Gn(12), Po: 33 },
    ];
  function ns(t, i) {
    if (t.getUTCFullYear() !== i.getUTCFullYear()) return 70;
    if (t.getUTCMonth() !== i.getUTCMonth()) return 60;
    if (t.getUTCDate() !== i.getUTCDate()) return 50;
    for (var n = is.length - 1; n >= 0; --n)
      if (
        Math.floor(i.getTime() / is[n].Hw) !==
        Math.floor(t.getTime() / is[n].Hw)
      )
        return is[n].Po;
    return 0;
  }
  function ss(t, i) {
    if ((void 0 === i && (i = 0), 0 !== t.length)) {
      for (
        var n = 0 === i ? null : t[i - 1].rt.So,
          s = null !== n ? new Date(1e3 * n) : null,
          h = 0,
          r = i;
        r < t.length;
        ++r
      ) {
        var e = t[r],
          u = new Date(1e3 * e.rt.So);
        null !== s && (e.Vo = ns(u, s)),
          (h += e.rt.So - (n || e.rt.So)),
          (n = e.rt.So),
          (s = u);
      }
      if (0 === i && t.length > 1) {
        var a = Math.ceil(h / (t.length - 1)),
          o = new Date(1e3 * (t[0].rt.So - a));
        t[0].Vo = ns(new Date(1e3 * t[0].rt.So), o);
      }
    }
  }
  function hs(t) {
    if (!vn(t)) throw new Error("time must be of type BusinessDay");
    var i = new Date(Date.UTC(t.year, t.month - 1, t.day, 0, 0, 0, 0));
    return { So: Math.round(i.getTime() / 1e3), Co: t };
  }
  function rs(t) {
    if (!_n(t)) throw new Error("time must be of type isUTCTimestamp");
    return { So: t };
  }
  function es(t) {
    return 0 === t.length ? null : vn(t[0].time) ? hs : rs;
  }
  function us(t) {
    return _n(t) ? rs(t) : vn(t) ? hs(t) : hs(as(t));
  }
  function as(t) {
    var i = new Date(t);
    if (isNaN(i.getTime()))
      throw new Error(
        "Invalid date string=".concat(t, ", expected format=yyyy-mm-dd")
      );
    return {
      day: i.getUTCDate(),
      month: i.getUTCMonth() + 1,
      year: i.getUTCFullYear(),
    };
  }
  function os(t) {
    N(t.time) && (t.time = as(t.time));
  }
  function ls(t) {
    return { vs: 0, Yw: new Map(), Ve: t };
  }
  function fs(t) {
    if (void 0 !== t && 0 !== t.length)
      return { $w: t[0].rt.So, Kw: t[t.length - 1].rt.So };
  }
  var cs = (function () {
    function t() {
      (this.Xw = new Map()),
        (this.Zw = new Map()),
        (this.Jw = new Map()),
        (this.Gw = []);
    }
    return (
      (t.prototype.p = function () {
        this.Xw.clear(), this.Zw.clear(), this.Jw.clear(), (this.Gw = []);
      }),
      (t.prototype.Qw = function (t, i) {
        var n = this,
          s = 0 !== this.Xw.size,
          h = !1,
          r = this.Zw.get(t);
        if (void 0 !== r)
          if (1 === this.Zw.size) (s = !1), (h = !0), this.Xw.clear();
          else
            for (var u = 0, a = this.Gw; u < a.length; u++) {
              a[u].pointData.Yw.delete(t) && (h = !0);
            }
        var o = [];
        if (0 !== i.length) {
          !(function (t) {
            t.forEach(os);
          })(i);
          var l = e(es(i)),
            f = Jn(t.Wr());
          o = i.map(function (i) {
            var s = l(i.time),
              r = n.Xw.get(s.So);
            void 0 === r && ((r = ls(s)), n.Xw.set(s.So, r), (h = !0));
            var e = f(s, r.vs, i);
            return r.Yw.set(t, e), e;
          });
        }
        s && this.tM(), this.iM(t, o);
        var c = -1;
        if (h) {
          var v = [];
          this.Xw.forEach(function (t) {
            v.push({ Vo: 0, rt: t.Ve, pointData: t });
          }),
            v.sort(function (t, i) {
              return t.rt.So - i.rt.So;
            }),
            (c = this.nM(v));
        }
        return this.sM(
          t,
          c,
          (function (t, i) {
            var n = fs(t),
              s = fs(i);
            if (void 0 !== n && void 0 !== s)
              return { Ae: n.Kw >= s.Kw && n.$w >= s.$w };
          })(this.Zw.get(t), r)
        );
      }),
      (t.prototype.Yf = function (t) {
        return this.Qw(t, []);
      }),
      (t.prototype.hM = function (t, i) {
        os(i);
        var n = e(es([i]))(i.time),
          s = this.Jw.get(t);
        if (void 0 !== s && n.So < s.So)
          throw new Error(
            "Cannot update oldest data, last time="
              .concat(s.So, ", new time=")
              .concat(n.So)
          );
        var h = this.Xw.get(n.So),
          r = void 0 === h;
        void 0 === h && ((h = ls(n)), this.Xw.set(n.So, h));
        var u = Jn(t.Wr())(n, h.vs, i);
        h.Yw.set(t, u), this.rM(t, u);
        var a = { Ae: Kn(u) };
        if (!r) return this.sM(t, -1, a);
        var o = { Vo: 0, rt: h.Ve, pointData: h },
          l = ct(this.Gw, o.rt.So, function (t, i) {
            return t.rt.So < i;
          });
        this.Gw.splice(l, 0, o);
        for (var f = l; f < this.Gw.length; ++f) vs(this.Gw[f].pointData, f);
        return ss(this.Gw, l), this.sM(t, l, a);
      }),
      (t.prototype.rM = function (t, i) {
        var n = this.Zw.get(t);
        void 0 === n && ((n = []), this.Zw.set(t, n));
        var s = 0 !== n.length ? n[n.length - 1] : null;
        null === s || i.rt.So > s.rt.So
          ? Kn(i) && n.push(i)
          : Kn(i)
          ? (n[n.length - 1] = i)
          : n.splice(-1, 1),
          this.Jw.set(t, i.rt);
      }),
      (t.prototype.iM = function (t, i) {
        0 !== i.length
          ? (this.Zw.set(t, i.filter(Kn)), this.Jw.set(t, i[i.length - 1].rt))
          : (this.Zw.delete(t), this.Jw.delete(t));
      }),
      (t.prototype.tM = function () {
        for (var t = 0, i = this.Gw; t < i.length; t++) {
          var n = i[t];
          0 === n.pointData.Yw.size && this.Xw.delete(n.rt.So);
        }
      }),
      (t.prototype.nM = function (t) {
        for (var i = -1, n = 0; n < this.Gw.length && n < t.length; ++n) {
          var s = this.Gw[n],
            h = t[n];
          if (s.rt.So !== h.rt.So) {
            i = n;
            break;
          }
          (h.Vo = s.Vo), vs(h.pointData, n);
        }
        if (
          (-1 === i &&
            this.Gw.length !== t.length &&
            (i = Math.min(this.Gw.length, t.length)),
          -1 === i)
        )
          return -1;
        for (n = i; n < t.length; ++n) vs(t[n].pointData, n);
        return ss(t, i), (this.Gw = t), i;
      }),
      (t.prototype.eM = function () {
        if (0 === this.Zw.size) return null;
        var t = 0;
        return (
          this.Zw.forEach(function (i) {
            0 !== i.length && (t = Math.max(t, i[i.length - 1].vs));
          }),
          t
        );
      }),
      (t.prototype.sM = function (t, i, n) {
        var s = { uM: new Map(), bt: { ml: this.eM() } };
        if (-1 !== i)
          this.Zw.forEach(function (i, h) {
            s.uM.set(h, { gh: i, aM: h === t ? n : void 0 });
          }),
            this.Zw.has(t) || s.uM.set(t, { gh: [], aM: n }),
            (s.bt.oM = this.Gw),
            (s.bt.lM = i);
        else {
          var h = this.Zw.get(t);
          s.uM.set(t, { gh: h || [], aM: n });
        }
        return s;
      }),
      t
    );
  })();
  function vs(t, i) {
    (t.vs = i),
      t.Yw.forEach(function (t) {
        t.vs = i;
      });
  }
  var _s = {
      color: "#FF0000",
      price: 0,
      lineStyle: 2,
      lineWidth: 1,
      lineVisible: !0,
      axisLabelVisible: !0,
      title: "",
    },
    ds = (function () {
      function t(t) {
        this.Lr = t;
      }
      return (
        (t.prototype.applyOptions = function (t) {
          this.Lr.Pr(t);
        }),
        (t.prototype.options = function () {
          return this.Lr.R();
        }),
        (t.prototype.fM = function () {
          return this.Lr;
        }),
        t
      );
    })();
  function ws(t) {
    var i = t.overlay,
      n = (function (t, i) {
        var n = {};
        for (var s in t)
          Object.prototype.hasOwnProperty.call(t, s) &&
            i.indexOf(s) < 0 &&
            (n[s] = t[s]);
        if (null != t && "function" == typeof Object.getOwnPropertySymbols) {
          var h = 0;
          for (s = Object.getOwnPropertySymbols(t); h < s.length; h++)
            i.indexOf(s[h]) < 0 &&
              Object.prototype.propertyIsEnumerable.call(t, s[h]) &&
              (n[s[h]] = t[s[h]]);
        }
        return n;
      })(t, ["overlay"]);
    return i && (n.priceScaleId = ""), n;
  }
  var Ms = (function () {
      function t(t, i, n) {
        (this.Kn = t), (this.cM = i), (this.vM = n);
      }
      return (
        (t.prototype.priceFormatter = function () {
          return this.Kn.qe();
        }),
        (t.prototype.priceToCoordinate = function (t) {
          var i = this.Kn.kt();
          return null === i ? null : this.Kn.Ct().Nt(t, i.St);
        }),
        (t.prototype.coordinateToPrice = function (t) {
          var i = this.Kn.kt();
          return null === i ? null : this.Kn.Ct().qi(t, i.St);
        }),
        (t.prototype.barsInLogicalRange = function (t) {
          if (null === t) return null;
          var i = new nn(new Ji(t.from, t.to)).jo(),
            n = this.Kn.an();
          if (n.wi()) return null;
          var s = n.ne(i.In(), 1),
            h = n.ne(i.jn(), -1),
            r = e(n.Qr()),
            u = e(n.un());
          if (null !== s && null !== h && s.vs > h.vs)
            return { barsBefore: t.from - r, barsAfter: u - t.to };
          var a = {
            barsBefore: null === s || s.vs === r ? t.from - r : s.vs - r,
            barsAfter: null === h || h.vs === u ? u - t.to : u - h.vs,
          };
          return (
            null !== s &&
              null !== h &&
              ((a.from = s.rt.Co || s.rt.So), (a.to = h.rt.Co || h.rt.So)),
            a
          );
        }),
        (t.prototype.setData = function (t) {
          this.Kn.Wr(), this.cM._M(this.Kn, t);
        }),
        (t.prototype.update = function (t) {
          this.Kn.Wr(), this.cM.dM(this.Kn, t);
        }),
        (t.prototype.setMarkers = function (t) {
          var i = t.map(function (t) {
            return m(m({}, t), { time: us(t.time) });
          });
          this.Kn.Le(i);
        }),
        (t.prototype.applyOptions = function (t) {
          var i = ws(t);
          this.Kn.Pr(i);
        }),
        (t.prototype.options = function () {
          return S(this.Kn.R());
        }),
        (t.prototype.priceScale = function () {
          return this.vM.priceScale(this.Kn.Ct().Ke());
        }),
        (t.prototype.createPriceLine = function (t) {
          var i = y(S(_s), t),
            n = this.Kn.Ee(i);
          return new ds(n);
        }),
        (t.prototype.removePriceLine = function (t) {
          this.Kn.Oe(t.fM());
        }),
        (t.prototype.seriesType = function () {
          return this.Kn.Wr();
        }),
        t
      );
    })(),
    bs = (function (t) {
      function i() {
        return (null !== t && t.apply(this, arguments)) || this;
      }
      return (
        b(i, t),
        (i.prototype.applyOptions = function (i) {
          cn(i), t.prototype.applyOptions.call(this, i);
        }),
        i
      );
    })(Ms),
    ms = {
      autoScale: !0,
      mode: 0,
      invertScale: !1,
      alignLabels: !0,
      borderVisible: !0,
      borderColor: "#2B2B43",
      entireTextOnly: !1,
      visible: !1,
      drawTicks: !0,
      scaleMargins: { bottom: 0.1, top: 0.2 },
    },
    gs = {
      color: "rgba(0, 0, 0, 0)",
      visible: !1,
      fontSize: 48,
      fontFamily: A,
      fontStyle: "",
      text: "",
      horzAlign: "center",
      vertAlign: "center",
    },
    ps = {
      width: 0,
      height: 0,
      layout: {
        background: { type: "solid", color: "#FFFFFF" },
        textColor: "#191919",
        fontSize: 11,
        fontFamily: A,
      },
      crosshair: {
        vertLine: {
          color: "#758696",
          width: 1,
          style: 3,
          visible: !0,
          labelVisible: !0,
          labelBackgroundColor: "#4c525e",
        },
        horzLine: {
          color: "#758696",
          width: 1,
          style: 3,
          visible: !0,
          labelVisible: !0,
          labelBackgroundColor: "#4c525e",
        },
        mode: 1,
      },
      grid: {
        vertLines: { color: "#D6DCDE", style: 0, visible: !0 },
        horzLines: { color: "#D6DCDE", style: 0, visible: !0 },
      },
      overlayPriceScales: m({}, ms),
      leftPriceScale: m(m({}, ms), { visible: !1 }),
      rightPriceScale: m(m({}, ms), { visible: !0 }),
      timeScale: {
        rightOffset: 0,
        barSpacing: 6,
        minBarSpacing: 0.5,
        fixLeftEdge: !1,
        fixRightEdge: !1,
        lockVisibleTimeRangeOnResize: !1,
        rightBarStaysOnScroll: !1,
        borderVisible: !0,
        borderColor: "#2B2B43",
        visible: !0,
        timeVisible: !1,
        secondsVisible: !0,
        shiftVisibleRangeOnNewBar: !0,
      },
      watermark: gs,
      localization: {
        locale: Nn ? navigator.language : "",
        dateFormat: "dd MMM 'yy",
      },
      handleScroll: {
        mouseWheel: !0,
        pressedMouseMove: !0,
        horzTouchDrag: !0,
        vertTouchDrag: !0,
      },
      handleScale: {
        axisPressedMouseMove: { time: !0, price: !0 },
        axisDoubleClickReset: !0,
        mouseWheel: !0,
        pinch: !0,
      },
      kineticScroll: { mouse: !1, touch: !0 },
      trackingMode: { exitMode: 1 },
    },
    ys = {
      upColor: "#26a69a",
      downColor: "#ef5350",
      wickVisible: !0,
      borderVisible: !0,
      borderColor: "#378658",
      borderUpColor: "#26a69a",
      borderDownColor: "#ef5350",
      wickColor: "#737375",
      wickUpColor: "#26a69a",
      wickDownColor: "#ef5350",
    },
    ks = {
      upColor: "#26a69a",
      downColor: "#ef5350",
      openVisible: !0,
      thinBars: !0,
    },
    xs = {
      color: "#2196f3",
      lineStyle: 0,
      lineWidth: 3,
      lineType: 0,
      crosshairMarkerVisible: !0,
      crosshairMarkerRadius: 4,
      crosshairMarkerBorderColor: "",
      crosshairMarkerBackgroundColor: "",
      lastPriceAnimation: 0,
    },
    Ns = {
      topColor: "rgba( 46, 220, 135, 0.4)",
      bottomColor: "rgba( 40, 221, 100, 0)",
      lineColor: "#33D778",
      lineStyle: 0,
      lineWidth: 3,
      lineType: 0,
      crosshairMarkerVisible: !0,
      crosshairMarkerRadius: 4,
      crosshairMarkerBorderColor: "",
      crosshairMarkerBackgroundColor: "",
      lastPriceAnimation: 0,
    },
    Cs = {
      baseValue: { type: "price", price: 0 },
      topFillColor1: "rgba(38, 166, 154, 0.28)",
      topFillColor2: "rgba(38, 166, 154, 0.05)",
      topLineColor: "rgba(38, 166, 154, 1)",
      bottomFillColor1: "rgba(239, 83, 80, 0.05)",
      bottomFillColor2: "rgba(239, 83, 80, 0.28)",
      bottomLineColor: "rgba(239, 83, 80, 1)",
      lineWidth: 3,
      lineStyle: 0,
      crosshairMarkerVisible: !0,
      crosshairMarkerRadius: 4,
      crosshairMarkerBorderColor: "",
      crosshairMarkerBackgroundColor: "",
      lastPriceAnimation: 0,
    },
    Ss = { color: "#26a69a", base: 0 },
    Ts = {
      title: "",
      visible: !0,
      lastValueVisible: !0,
      priceLineVisible: !0,
      priceLineSource: 0,
      priceLineWidth: 1,
      priceLineColor: "",
      priceLineStyle: 2,
      baseLineVisible: !0,
      baseLineWidth: 1,
      baseLineColor: "#B2B5BE",
      baseLineStyle: 0,
      priceFormat: { type: "price", precision: 2, minMove: 0.01 },
    },
    Ds = (function () {
      function t(t, i) {
        (this.wM = t), (this.MM = i);
      }
      return (
        (t.prototype.applyOptions = function (t) {
          this.wM.jt().xf(this.MM, t);
        }),
        (t.prototype.options = function () {
          return this._i().R();
        }),
        (t.prototype.width = function () {
          return tt(this.MM)
            ? this.wM.Ow("left" === this.MM ? "left" : "right")
            : 0;
        }),
        (t.prototype._i = function () {
          return e(this.wM.jt().Nf(this.MM)).Ct;
        }),
        t
      );
    })(),
    As = (function () {
      function t(t, i) {
        (this.bM = new p()),
          (this.Go = new p()),
          (this.Zd = new p()),
          (this.gi = t),
          (this.Da = t.bt()),
          (this.xw = i),
          this.Da.Fl().u(this.mM.bind(this)),
          this.Da.Vl().u(this.gM.bind(this)),
          this.xw.hw().u(this.pM.bind(this));
      }
      return (
        (t.prototype.p = function () {
          this.Da.Fl().M(this),
            this.Da.Vl().M(this),
            this.xw.hw().M(this),
            this.bM.p(),
            this.Go.p(),
            this.Zd.p();
        }),
        (t.prototype.scrollPosition = function () {
          return this.Da.xl();
        }),
        (t.prototype.scrollToPosition = function (t, i) {
          i ? this.Da.Ol(t, 1e3) : this.gi.yn(t);
        }),
        (t.prototype.scrollToRealTime = function () {
          this.Da.El();
        }),
        (t.prototype.getVisibleRange = function () {
          var t,
            i,
            n = this.Da.cl();
          return null === n
            ? null
            : {
                from: null !== (t = n.from.Co) && void 0 !== t ? t : n.from.So,
                to: null !== (i = n.to.Co) && void 0 !== i ? i : n.to.So,
              };
        }),
        (t.prototype.setVisibleRange = function (t) {
          var i = { from: us(t.from), to: us(t.to) },
            n = this.Da.wl(i);
          this.gi.$f(n);
        }),
        (t.prototype.getVisibleLogicalRange = function () {
          var t = this.Da.fl();
          return null === t ? null : { from: t.In(), to: t.jn() };
        }),
        (t.prototype.setVisibleLogicalRange = function (t) {
          h(t.from <= t.to, "The from index cannot be after the to index."),
            this.gi.$f(t);
        }),
        (t.prototype.resetTimeScale = function () {
          this.gi.gn();
        }),
        (t.prototype.fitContent = function () {
          this.gi.zl();
        }),
        (t.prototype.logicalToCoordinate = function (t) {
          var i = this.gi.bt();
          return i.wi() ? null : i.At(t);
        }),
        (t.prototype.coordinateToLogical = function (t) {
          return this.Da.wi() ? null : this.Da.gl(t);
        }),
        (t.prototype.timeToCoordinate = function (t) {
          var i = us(t),
            n = this.Da.Ze(i, !1);
          return null === n ? null : this.Da.At(n);
        }),
        (t.prototype.coordinateToTime = function (t) {
          var i,
            n = this.gi.bt(),
            s = n.gl(t),
            h = n.pi(s);
          return null === h
            ? null
            : null !== (i = h.Co) && void 0 !== i
            ? i
            : h.So;
        }),
        (t.prototype.width = function () {
          return this.xw.Ld().Ot;
        }),
        (t.prototype.height = function () {
          return this.xw.Ld().Ft;
        }),
        (t.prototype.subscribeVisibleTimeRangeChange = function (t) {
          this.bM.u(t);
        }),
        (t.prototype.unsubscribeVisibleTimeRangeChange = function (t) {
          this.bM._(t);
        }),
        (t.prototype.subscribeVisibleLogicalRangeChange = function (t) {
          this.Go.u(t);
        }),
        (t.prototype.unsubscribeVisibleLogicalRangeChange = function (t) {
          this.Go._(t);
        }),
        (t.prototype.subscribeSizeChange = function (t) {
          this.Zd.u(t);
        }),
        (t.prototype.unsubscribeSizeChange = function (t) {
          this.Zd._(t);
        }),
        (t.prototype.applyOptions = function (t) {
          this.Da.Pr(t);
        }),
        (t.prototype.options = function () {
          return S(this.Da.R());
        }),
        (t.prototype.mM = function () {
          this.bM.g() && this.bM.m(this.getVisibleRange());
        }),
        (t.prototype.gM = function () {
          this.Go.g() && this.Go.m(this.getVisibleLogicalRange());
        }),
        (t.prototype.pM = function (t) {
          this.Zd.m(t.Ot, t.Ft);
        }),
        t
      );
    })();
  function Bs(t) {
    if (void 0 !== t && "custom" !== t.type) {
      var i = t;
      void 0 !== i.minMove &&
        void 0 === i.precision &&
        (i.precision = (function (t) {
          if (t >= 1) return 0;
          for (var i = 0; i < 8; i++) {
            var n = Math.round(t);
            if (Math.abs(n - t) < 1e-8) return i;
            t *= 10;
          }
          return i;
        })(i.minMove));
    }
  }
  function Ls(t) {
    return (
      (function (t) {
        if (C(t.handleScale)) {
          var i = t.handleScale;
          t.handleScale = {
            axisDoubleClickReset: i,
            axisPressedMouseMove: { time: i, price: i },
            mouseWheel: i,
            pinch: i,
          };
        } else if (
          void 0 !== t.handleScale &&
          C(t.handleScale.axisPressedMouseMove)
        ) {
          var n = t.handleScale.axisPressedMouseMove;
          t.handleScale.axisPressedMouseMove = { time: n, price: n };
        }
        var s = t.handleScroll;
        C(s) &&
          (t.handleScroll = {
            horzTouchDrag: s,
            vertTouchDrag: s,
            mouseWheel: s,
            pressedMouseMove: s,
          });
      })(t),
      (function (t) {
        if (t.priceScale) {
          (t.leftPriceScale = t.leftPriceScale || {}),
            (t.rightPriceScale = t.rightPriceScale || {});
          var i = t.priceScale.position;
          delete t.priceScale.position,
            (t.leftPriceScale = y(t.leftPriceScale, t.priceScale)),
            (t.rightPriceScale = y(t.rightPriceScale, t.priceScale)),
            "left" === i &&
              ((t.leftPriceScale.visible = !0),
              (t.rightPriceScale.visible = !1)),
            "right" === i &&
              ((t.leftPriceScale.visible = !1),
              (t.rightPriceScale.visible = !0)),
            "none" === i &&
              ((t.leftPriceScale.visible = !1),
              (t.rightPriceScale.visible = !1)),
            (t.overlayPriceScales = t.overlayPriceScales || {}),
            void 0 !== t.priceScale.invertScale &&
              (t.overlayPriceScales.invertScale = t.priceScale.invertScale),
            void 0 !== t.priceScale.scaleMargins &&
              (t.overlayPriceScales.scaleMargins = t.priceScale.scaleMargins);
        }
      })(t),
      (function (t) {
        t.layout &&
          t.layout.backgroundColor &&
          !t.layout.background &&
          (t.layout.background = {
            type: "solid",
            color: t.layout.backgroundColor,
          });
      })(t),
      t
    );
  }
  var Es = (function () {
    function t(t, i) {
      var n = this;
      (this.yM = new cs()),
        (this.kM = new Map()),
        (this.xM = new Map()),
        (this.NM = new p()),
        (this.CM = new p());
      var s = void 0 === i ? S(ps) : y(S(ps), Ls(i));
      (this.wM = new Hn(t, s)),
        this.wM.Sd().u(function (t) {
          n.NM.g() && n.NM.m(n.SM(t()));
        }, this),
        this.wM.Df().u(function (t) {
          n.CM.g() && n.CM.m(n.SM(t()));
        }, this);
      var h = this.wM.jt();
      this.TM = new As(h, this.wM.Dw());
    }
    return (
      (t.prototype.remove = function () {
        this.wM.Sd().M(this),
          this.wM.Df().M(this),
          this.TM.p(),
          this.wM.p(),
          this.kM.clear(),
          this.xM.clear(),
          this.NM.p(),
          this.CM.p(),
          this.yM.p();
      }),
      (t.prototype.resize = function (t, i, n) {
        this.wM.Nw(t, i, n);
      }),
      (t.prototype.addAreaSeries = function (t) {
        void 0 === t && (t = {}), Bs((t = ws(t)).priceFormat);
        var i = y(S(Ts), Ns, t),
          n = this.wM.jt().Uf("Area", i),
          s = new Ms(n, this, this);
        return this.kM.set(s, n), this.xM.set(n, s), s;
      }),
      (t.prototype.addBaselineSeries = function (t) {
        void 0 === t && (t = {}), Bs((t = ws(t)).priceFormat);
        var i = y(S(Ts), S(Cs), t),
          n = this.wM.jt().Uf("Baseline", i),
          s = new Ms(n, this, this);
        return this.kM.set(s, n), this.xM.set(n, s), s;
      }),
      (t.prototype.addBarSeries = function (t) {
        void 0 === t && (t = {}), Bs((t = ws(t)).priceFormat);
        var i = y(S(Ts), ks, t),
          n = this.wM.jt().Uf("Bar", i),
          s = new Ms(n, this, this);
        return this.kM.set(s, n), this.xM.set(n, s), s;
      }),
      (t.prototype.addCandlestickSeries = function (t) {
        void 0 === t && (t = {}), cn((t = ws(t))), Bs(t.priceFormat);
        var i = y(S(Ts), ys, t),
          n = this.wM.jt().Uf("Candlestick", i),
          s = new bs(n, this, this);
        return this.kM.set(s, n), this.xM.set(n, s), s;
      }),
      (t.prototype.addHistogramSeries = function (t) {
        void 0 === t && (t = {}), Bs((t = ws(t)).priceFormat);
        var i = y(S(Ts), Ss, t),
          n = this.wM.jt().Uf("Histogram", i),
          s = new Ms(n, this, this);
        return this.kM.set(s, n), this.xM.set(n, s), s;
      }),
      (t.prototype.addLineSeries = function (t) {
        void 0 === t && (t = {}), Bs((t = ws(t)).priceFormat);
        var i = y(S(Ts), xs, t),
          n = this.wM.jt().Uf("Line", i),
          s = new Ms(n, this, this);
        return this.kM.set(s, n), this.xM.set(n, s), s;
      }),
      (t.prototype.removeSeries = function (t) {
        var i = r(this.kM.get(t)),
          n = this.yM.Yf(i);
        this.wM.jt().Yf(i), this.DM(n), this.kM.delete(t), this.xM.delete(i);
      }),
      (t.prototype._M = function (t, i) {
        this.DM(this.yM.Qw(t, i));
      }),
      (t.prototype.dM = function (t, i) {
        this.DM(this.yM.hM(t, i));
      }),
      (t.prototype.subscribeClick = function (t) {
        this.NM.u(t);
      }),
      (t.prototype.unsubscribeClick = function (t) {
        this.NM._(t);
      }),
      (t.prototype.subscribeCrosshairMove = function (t) {
        this.CM.u(t);
      }),
      (t.prototype.unsubscribeCrosshairMove = function (t) {
        this.CM._(t);
      }),
      (t.prototype.priceScale = function (t) {
        return void 0 === t && (t = this.wM.jt().Kf()), new Ds(this.wM, t);
      }),
      (t.prototype.timeScale = function () {
        return this.TM;
      }),
      (t.prototype.applyOptions = function (t) {
        this.wM.Pr(Ls(t));
      }),
      (t.prototype.options = function () {
        return this.wM.R();
      }),
      (t.prototype.takeScreenshot = function () {
        return this.wM.Bw();
      }),
      (t.prototype.DM = function (t) {
        var i = this.wM.jt();
        i.jf(t.bt.ml, t.bt.oM, t.bt.lM),
          t.uM.forEach(function (t, i) {
            return i.Z(t.gh, t.aM);
          }),
          i.yl();
      }),
      (t.prototype.AM = function (t) {
        return r(this.xM.get(t));
      }),
      (t.prototype.SM = function (t) {
        var i = this,
          n = new Map();
        t.qw.forEach(function (t, s) {
          n.set(i.AM(s), t);
        });
        var s = void 0 === t.jw ? void 0 : this.AM(t.jw);
        return {
          time: t.rt && (t.rt.Co || t.rt.So),
          point: t.Iw,
          hoveredSeries: s,
          hoveredMarkerId: t.Uw,
          seriesPrices: n,
        };
      }),
      t
    );
  })();
  var Os = Object.freeze({
    __proto__: null,
    version: function () {
      return "3.8.0";
    },
    get LineStyle() {
      return i;
    },
    get LineType() {
      return t;
    },
    get TrackingModeExitMode() {
      return hn;
    },
    get CrosshairMode() {
      return H;
    },
    get PriceScaleMode() {
      return Vi;
    },
    get PriceLineSource() {
      return on;
    },
    get LastPriceAnimationMode() {
      return an;
    },
    get LasPriceAnimationMode() {
      return an;
    },
    get TickMarkType() {
      return Qi;
    },
    get ColorType() {
      return ln;
    },
    isBusinessDay: vn,
    isUTCTimestamp: _n,
    createChart: function (t, i) {
      var n;
      if (N(t)) {
        var s = document.getElementById(t);
        h(null !== s, "Cannot find element in DOM with id=".concat(t)), (n = s);
      } else n = t;
      return new Es(n, i);
    },
  });
  window.LightweightCharts = Os;
})();
