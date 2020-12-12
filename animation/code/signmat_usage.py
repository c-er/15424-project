from manimlib.imports import *
import os
import pyclbr
class PlotFunctions(GraphScene):
  CONFIG = {
    "x_min" : -2,
    "x_max" : 2,
    "y_min" : -0.5,
    "y_max" : 2,
    "graph_origin" : 2 * UP ,
    "function_color" : PURPLE ,
    "axes_color" : GREEN,
    "x_axis_label": "",
    "y_axis_label": "",
    "x_tick_frequency": 1,
    "y_tick_frequency": 1
  }

  CUSTOM_CONFIG = {
      "color": LIGHT_GREY,
      "x_min": -FRAME_X_RADIUS,
      "x_max": FRAME_X_RADIUS,
      "unit_size": 1,
      "include_ticks": False,  # this boolean controls tick generation
      "tick_size": 0.1,
      "tick_frequency": 1,
      # Defaults to value near x_min s.t. 0 is a tick
      # TODO, rename this
      "leftmost_tick": None,
      # Change name
      "numbers_with_elongated_ticks": [0],
      "include_numbers": False,
      "numbers_to_show": None,
      "longer_tick_multiple": 2,
      "number_at_center": 0,
      "number_scale_val": 0.75,
      "label_direction": DOWN,
      "line_to_number_buff": MED_SMALL_BUFF,
      "include_tip": False,
      "tip_width": 0.25,
      "tip_height": 0.25,
      "decimal_number_config": {"num_decimal_places": 0},
      "exclude_zero_from_default_numbers": False,
  }

  NumberLine.CONFIG = CUSTOM_CONFIG

  def construct(self):
    form = TexMobject(r"\forall x", r"\,[", r"(", r"p_1(x)", r"\geq 0", r"\,\wedge\,", r"p_2(x)", r"\geq 0", r")", r"\,\vee\,", r"(", r"p_3(x)", r"> 0", r")", "]\,?")
    form[3].set_color(BLUE)
    form[6].set_color(YELLOW)
    form[11].set_color(PURPLE)
    self.play(Write(form))
    self.wait(2)

    mat = TexMobject(r"\begin{array}{cccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\ p_1 & + & 0 & - & 0 & + \\ p_2 & - & 0 & + & + & + \\ p_3 & + & + & + & 0 & - \end{array}")
    mat.move_to(2.75 * UP)

    for i in range(24, 31):
      mat[0][i].set_color(BLUE)
    
    for i in range(31, 38):
      mat[0][i].set_color(YELLOW)
    
    for i in range(38, 45):
      mat[0][i].set_color(PURPLE)
  
    

    self.play(ApplyMethod(form.move_to, 3*DOWN), ShowCreation(mat), run_time=2)

    q = TextMobject(r"When $x \in (-\infty, x_1)$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))
    self.wait()

    v1 = 26
    v2 = 33
    v3 = 40

    miss = list(range(0, 7)) + [v1,v2,v3]
    l = []
    for i in range(len(mat[0])):
      if i not in miss:
        l.append(ApplyMethod(mat[0][i].set_opacity, 0.3))
    
    self.play(*l)
    self.wait()

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$+$")
    b1_text.set_color(BLUE)
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$-$")
    b2_text.set_color(YELLOW)
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$+$")
    b3_text.set_color(PURPLE)
    dc1 = mat[0][v1].deepcopy()
    dc2 = mat[0][v2].deepcopy()
    dc3 = mat[0][v3].deepcopy()
    self.play(GrowFromCenter(b1),Transform(dc1, b1_text))
    self.play(GrowFromCenter(b2),Transform(dc2, b2_text))
    self.play(GrowFromCenter(b3),Transform(dc3, b3_text))
    self.wait()

    b11 = Brace(VGroup(b1, b1_text, form[3], form[4]), UP)
    b21 = Brace(VGroup(b2, b2_text, form[6], form[7]), UP)
    b31 = Brace(VGroup(b3, b3_text, form[11], form[12]), UP)
    b31.align_to(b11, UP)
    b21.align_to(b11, UP)

    b11_text = b11.get_text(r"$\top$")
    b11_text.set_color(GREEN)

    b21_text = b21.get_text(r"$\bot$")
    b21_text.set_color(RED)

    b31_text = b31.get_text(r"$\top$")
    b31_text.set_color(GREEN)

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text))

    self.wait()

    top = TexMobject(r"\top")
    top.move_to(q[1])
    top.set_color(GREEN)
    self.play(ReplacementTransform(q[1], top))

    self.wait()

    l = []
    for i in range(len(mat[0])):
      l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    self.play(FadeOut(b11), FadeOut(b21), FadeOut(b31), FadeOut(b11_text), FadeOut(b21_text), FadeOut(b31_text),
      FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b1_text), FadeOut(b2_text), FadeOut(b3_text),
      FadeOut(q), FadeOut(top), FadeOut(dc1), FadeOut(dc2), FadeOut(dc3), *l)

    #### 2 ####

    q = TextMobject(r"When $x = x_1$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))
    self.wait()

    v1 = 27
    v2 = 34
    v3 = 41

    miss = list(range(7, 9)) + [v1,v2,v3]
    l = []
    for i in range(len(mat[0])):
      if i not in miss:
        l.append(ApplyMethod(mat[0][i].set_opacity, 0.3))
      else:
        l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    
    self.play(*l)
    self.wait()

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$0$")
    b1_text.set_color(BLUE)
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$0$")
    b2_text.set_color(YELLOW)
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$+$")
    b3_text.set_color(PURPLE)
    dc1 = mat[0][v1].deepcopy()
    dc2 = mat[0][v2].deepcopy()
    dc3 = mat[0][v3].deepcopy()
    self.play(GrowFromCenter(b1),Transform(dc1, b1_text))
    self.play(GrowFromCenter(b2),Transform(dc2, b2_text))
    self.play(GrowFromCenter(b3),Transform(dc3, b3_text))
    self.wait()

    b11 = Brace(VGroup(b1, b1_text, form[3], form[4]), UP)
    b21 = Brace(VGroup(b2, b2_text, form[6], form[7]), UP)
    b31 = Brace(VGroup(b3, b3_text, form[11], form[12]), UP)
    b11.align_to(b31, UP)
    b21.align_to(b31, UP)

    b11_text = b11.get_text(r"$\top$")
    b11_text.set_color(GREEN)

    b21_text = b21.get_text(r"$\top$")
    b21_text.set_color(GREEN)

    b31_text = b31.get_text(r"$\top$")
    b31_text.set_color(GREEN)

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text))

    self.wait()

    top = TexMobject(r"\top")
    top.move_to(q[1])
    top.set_color(GREEN)
    self.play(ReplacementTransform(q[1], top))

    self.wait()

    l = []
    for i in range(len(mat[0])):
      l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    self.play(FadeOut(b11), FadeOut(b21), FadeOut(b31), FadeOut(b11_text), FadeOut(b21_text), FadeOut(b31_text),
      FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b1_text), FadeOut(b2_text), FadeOut(b3_text),
      FadeOut(q), FadeOut(top), FadeOut(dc1), FadeOut(dc2), FadeOut(dc3), *l)

    #### 3 ####

    q = TextMobject(r"When $x \in (x_1, x_2)$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))
    self.wait()

    v1 = 28
    v2 = 35
    v3 = 42

    miss = list(range(9, 16)) + [v1,v2,v3]
    l = []
    for i in range(len(mat[0])):
      if i not in miss:
        l.append(ApplyMethod(mat[0][i].set_opacity, 0.3))
      else:
        l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    
    self.play(*l)
    self.wait()

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$-$")
    b1_text.set_color(BLUE)
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$+$")
    b2_text.set_color(YELLOW)
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$+$")
    b3_text.set_color(PURPLE)
    dc1 = mat[0][v1].deepcopy()
    dc2 = mat[0][v2].deepcopy()
    dc3 = mat[0][v3].deepcopy()
    self.play(GrowFromCenter(b1),Transform(dc1, b1_text))
    self.play(GrowFromCenter(b2),Transform(dc2, b2_text))
    self.play(GrowFromCenter(b3),Transform(dc3, b3_text))
    self.wait()

    b11 = Brace(VGroup(b1, b1_text, form[3], form[4]), UP)
    b21 = Brace(VGroup(b2, b2_text, form[6], form[7]), UP)
    b31 = Brace(VGroup(b3, b3_text, form[11], form[12]), UP)
    b11.align_to(b31, UP)
    b21.align_to(b31, UP)

    b11_text = b11.get_text(r"$\bot$")
    b11_text.set_color(RED)

    b21_text = b21.get_text(r"$\top$")
    b21_text.set_color(GREEN)

    b31_text = b31.get_text(r"$\top$")
    b31_text.set_color(GREEN)

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text))

    self.wait()

    top = TexMobject(r"\top")
    top.move_to(q[1])
    top.set_color(GREEN)
    self.play(ReplacementTransform(q[1], top))

    self.wait()

    l = []
    for i in range(len(mat[0])):
      l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    self.play(FadeOut(b11), FadeOut(b21), FadeOut(b31), FadeOut(b11_text), FadeOut(b21_text), FadeOut(b31_text),
      FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b1_text), FadeOut(b2_text), FadeOut(b3_text),
      FadeOut(q), FadeOut(top), FadeOut(dc1), FadeOut(dc2), FadeOut(dc3), *l)

    #### 4 ####

    q = TextMobject(r"When $x = x_2$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))
    self.wait()

    v1 = 29
    v2 = 36
    v3 = 43

    miss = list(range(16, 18)) + [v1,v2,v3]
    l = []
    for i in range(len(mat[0])):
      if i not in miss:
        l.append(ApplyMethod(mat[0][i].set_opacity, 0.3))
      else:
        l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    
    self.play(*l)
    self.wait()

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$0$")
    b1_text.set_color(BLUE)
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$+$")
    b2_text.set_color(YELLOW)
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$0$")
    b3_text.set_color(PURPLE)
    dc1 = mat[0][v1].deepcopy()
    dc2 = mat[0][v2].deepcopy()
    dc3 = mat[0][v3].deepcopy()
    self.play(GrowFromCenter(b1),Transform(dc1, b1_text))
    self.play(GrowFromCenter(b2),Transform(dc2, b2_text))
    self.play(GrowFromCenter(b3),Transform(dc3, b3_text))
    self.wait()

    b11 = Brace(VGroup(b1, b1_text, form[3], form[4]), UP)
    b21 = Brace(VGroup(b2, b2_text, form[6], form[7]), UP)
    b31 = Brace(VGroup(b3, b3_text, form[11], form[12]), UP)
    b31.align_to(b21, UP)
    b11.align_to(b21, UP)

    b11_text = b11.get_text(r"$\top$")
    b11_text.set_color(GREEN)

    b21_text = b21.get_text(r"$\top$")
    b21_text.set_color(GREEN)

    b31_text = b31.get_text(r"$\bot$")
    b31_text.set_color(RED)

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text))

    self.wait()

    top = TexMobject(r"\top")
    top.move_to(q[1])
    top.set_color(GREEN)
    self.play(ReplacementTransform(q[1], top))

    self.wait()
    
    l = []
    for i in range(len(mat[0])):
      l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    self.play(FadeOut(b11), FadeOut(b21), FadeOut(b31), FadeOut(b11_text), FadeOut(b21_text), FadeOut(b31_text),
      FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b1_text), FadeOut(b2_text), FadeOut(b3_text),
      FadeOut(q), FadeOut(top), FadeOut(dc1), FadeOut(dc2), FadeOut(dc3), *l)

    #### 5 ####

    q = TextMobject(r"When $x \in (x_2, \infty)$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))
    self.wait()

    v1 = 30
    v2 = 37
    v3 = 44

    miss = list(range(18, 24)) + [v1,v2,v3]
    l = []
    for i in range(len(mat[0])):
      if i not in miss:
        l.append(ApplyMethod(mat[0][i].set_opacity, 0.3))
      else:
        l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    
    self.play(*l)
    self.wait()

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$+$")
    b1_text.set_color(BLUE)
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$+$")
    b2_text.set_color(YELLOW)
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$-$")
    b3_text.set_color(PURPLE)
    dc1 = mat[0][v1].deepcopy()
    dc2 = mat[0][v2].deepcopy()
    dc3 = mat[0][v3].deepcopy()
    self.play(GrowFromCenter(b1),Transform(dc1, b1_text))
    self.play(GrowFromCenter(b2),Transform(dc2, b2_text))
    self.play(GrowFromCenter(b3),Transform(dc3, b3_text))
    self.wait()

    b11 = Brace(VGroup(b1, b1_text, form[3], form[4]), UP)
    b21 = Brace(VGroup(b2, b2_text, form[6], form[7]), UP)
    b31 = Brace(VGroup(b3, b3_text, form[11], form[12]), UP)
    b31.align_to(b11, UP)
    b21.align_to(b11, UP)

    b11_text = b11.get_text(r"$\top$")
    b11_text.set_color(GREEN)

    b21_text = b21.get_text(r"$\top$")
    b21_text.set_color(GREEN)

    b31_text = b31.get_text(r"$\bot$")
    b31_text.set_color(RED)

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text))

    self.wait()

    top = TexMobject(r"\top")
    top.move_to(q[1])
    top.set_color(GREEN)
    self.play(ReplacementTransform(q[1], top))

    self.wait(2)

    l = []
    for i in range(len(mat[0])):
      l.append(ApplyMethod(mat[0][i].set_opacity, 1))
    self.play(FadeOut(b11), FadeOut(b21), FadeOut(b31), FadeOut(b11_text), FadeOut(b21_text), FadeOut(b31_text),
      FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeOut(b1_text), FadeOut(b2_text), FadeOut(b3_text),
      FadeOut(q), FadeOut(top), FadeOut(dc1), FadeOut(dc2), FadeOut(dc3), FadeOut(mat), ApplyMethod(form.move_to, ORIGIN))

    self.wait()

    form2 = TexMobject(r"\models", r"\forall x", r"\,[", r"(", r"p_1(x)", r"\geq 0", r"\,\wedge\,", r"p_2(x)", r"\geq 0", r")", r"\,\vee\,", r"(", r"p_3(x)", r"> 0", r")", "]")
    form2[0].set_color(GREEN)
    form2[4].set_color(BLUE)
    form2[7].set_color(YELLOW)
    form2[12].set_color(PURPLE)
    self.play(ReplacementTransform(form, form2))





    self.wait(2)