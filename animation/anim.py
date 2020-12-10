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
    form = TexMobject(r"\forall x", r"\,[", r"(", r"p_1(x)", r"\geq 0", r"\,\wedge\,", r"p_2(x)", r"\geq 0", r")", r"\,\vee\,", r"(", r"p_3(x)", r"> 0", r")", "]", "?")
    form[3].set_color(BLUE)
    form[6].set_color(YELLOW)
    form[11].set_color(PURPLE)
    self.play(Write(form))
    self.wait(2)
    self.play(FadeOut(form))

    # axes = Axes(x_min=-2, x_max=2, y_min=-1.2, y_max=2, color=GREEN)
    self.setup_axes(animate=True)

    gp1 = self.get_graph(self.p1,color=BLUE)
    gp1_lab = self.get_graph_label(gp1, label=r"p_1")

    gp2 = self.get_graph(self.p2,color=YELLOW)
    gp2_lab = self.get_graph_label(gp2, label=r"p_2", direction=UP/2)

    gp3 = self.get_graph(self.p3,color=PURPLE)
    gp3_lab = self.get_graph_label(gp3, label=r"p_3")

    root1 = Dot(color=WHITE).move_to(self.coords_to_point(-1,0))
    root1_lab = TexMobject(r"x_1")
    root1_lab.next_to(root1,DOWN)

    root2 = Dot(color=WHITE).move_to(self.coords_to_point(1,0))
    root2_lab = TexMobject(r"x_2")
    root2_lab.next_to(root2,DOWN)

    self.play(ShowCreation(gp1), ShowCreation(gp2),ShowCreation(gp3))
    self.play(ShowCreation(gp1_lab), ShowCreation(gp2_lab), ShowCreation(gp3_lab))
    self.play(ShowCreation(root1),ShowCreation(root2))
    self.play(ShowCreation(root1_lab),ShowCreation(root2_lab))

    self.wait()

    mat = TexMobject(r"\begin{array}{cccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\ p_1 \\ p_2 \\ p_3 \end{array}")
    mat.move_to(2*DOWN)
    
    self.play(Write(mat))

    self.wait()

    self.play(ApplyMethod(gp1.set_color, GREY), ApplyMethod(gp2.set_color, GREY), ApplyMethod(gp3.set_color, GREY))
    # self.play(FadeOut(gp1),FadeOut(gp2),FadeOut(gp3),FadeOut(gp1_lab),FadeOut(gp2_lab),FadeOut(gp3_lab))

    gp1_1 = self.get_graph(self.p1,color=BLUE,x_min=-2,x_max=-1)
    gp2_1 = self.get_graph(self.p2,color=YELLOW,x_min=-2,x_max=-1)
    gp3_1 = self.get_graph(self.p3,color=PURPLE,x_min=-2,x_max=-1)

    mat1 = TexMobject(r"\begin{array}{cccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\ p_1 & + & 0 \\ p_2 & - & 0 \\ p_3 & + & + \end{array}")
    mat1.move_to(2*DOWN)
    
    self.play(ShowCreation(gp1_1),ShowCreation(gp2_1),ShowCreation(gp3_1))
    self.play(Write(mat1))
    self.play(FadeOut(gp1_1), FadeOut(gp2_1), FadeOut(gp3_1))
    self.wait()

    gp1_2 = self.get_graph(self.p1,color=BLUE,x_min=-1,x_max=1)
    gp2_2 = self.get_graph(self.p2,color=YELLOW,x_min=-1,x_max=1)
    gp3_2 = self.get_graph(self.p3,color=PURPLE,x_min=-1,x_max=1)

    mat2 = TexMobject(r"\begin{array}{cccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\ p_1 & + & 0 & - & 0 \\ p_2 & - & 0 & + & + \\ p_3 & + & + & + & 0 \end{array}")
    mat2.move_to(2*DOWN)
    
    self.play(ShowCreation(gp1_2),ShowCreation(gp2_2),ShowCreation(gp3_2))
    self.play(Write(mat2))
    self.play(FadeOut(gp1_2), FadeOut(gp2_2), FadeOut(gp3_2))
    self.wait()

    gp1_3 = self.get_graph(self.p1,color=BLUE,x_min=1,x_max=2)
    gp2_3 = self.get_graph(self.p2,color=YELLOW,x_min=1,x_max=2)
    gp3_3 = self.get_graph(self.p3,color=PURPLE,x_min=1,x_max=2)

    mat3 = TexMobject(r"\begin{array}{cccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\ p_1 & + & 0 & - & 0 & + \\ p_2 & - & 0 & + & + & + \\ p_3 & + & + & + & 0 & - \end{array}")
    mat3.move_to(2*DOWN)
    
    self.play(ShowCreation(gp1_3),ShowCreation(gp2_3),ShowCreation(gp3_3))
    self.play(Write(mat3))
    self.play(FadeOut(gp1_3), FadeOut(gp2_3), FadeOut(gp3_3))
    self.wait()

    self.play(FadeOut(self.axes), FadeOut(gp1), FadeOut(gp1_lab), FadeOut(gp2), FadeOut(gp2_lab), FadeOut(gp3), FadeOut(gp3_lab), FadeOut(root1), FadeOut(root2), FadeOut(root1_lab), FadeOut(root2_lab), FadeOut(mat), FadeOut(mat1), FadeOut(mat2))
    self.play(ApplyMethod(mat3.move_to, 2.75*UP))


    form = TexMobject(r"\forall x", r"\,[", r"(", r"p_1(x)", r"\geq 0", r"\,\wedge\,", r"p_2(x)", r"\geq 0", r")", r"\,\vee\,", r"(", r"p_3(x)", r"> 0", r")", "]\,?")
    form.move_to(3*DOWN)
    form[3].set_color(BLUE)
    form[6].set_color(YELLOW)
    form[11].set_color(PURPLE)
    self.play(Write(form))

    q = TextMobject(r"When $x \in (-\infty, x_1)$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$+$")
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$-$")
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$+$")
    self.play(GrowFromCenter(b1),Write(b1_text),GrowFromCenter(b2),Write(b2_text),GrowFromCenter(b3),Write(b3_text), run_time=2)

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

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text), run_time=2)


    q2 = TextMobject(r"When $x \in (-\infty, x_1)$: ", r"$\top$")
    q2.set_color(GREEN)
    q2.move_to(UP)
    self.play(ReplacementTransform(q, q2))

    self.wait()

    self.play(FadeOut(b1),FadeOut(b1_text),FadeOut(b2),FadeOut(b2_text),FadeOut(b3),FadeOut(b3_text),FadeOut(b11),FadeOut(b11_text),FadeOut(b21),FadeOut(b21_text),FadeOut(b31),FadeOut(b31_text),FadeOut(q2))

    # 2

    q = TextMobject(r"When $x = x_1$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$0$")
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$0$")
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$+$")
    self.play(GrowFromCenter(b1),Write(b1_text),GrowFromCenter(b2),Write(b2_text),GrowFromCenter(b3),Write(b3_text), run_time=2)
    

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

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text), run_time=2)

    q2 = TextMobject(r"When $x = x_1$: ", r"$\top$")
    q2.set_color(GREEN)
    q2.move_to(UP)
    self.play(ReplacementTransform(q, q2))

    self.wait()

    self.play(FadeOut(b1),FadeOut(b1_text),FadeOut(b2),FadeOut(b2_text),FadeOut(b3),FadeOut(b3_text),FadeOut(b11),FadeOut(b11_text),FadeOut(b21),FadeOut(b21_text),FadeOut(b31),FadeOut(b31_text),FadeOut(q2))

    # 3
    q = TextMobject(r"When $x \in (x_1, x_2)$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$-$")
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$+$")
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$+$")
    self.play(GrowFromCenter(b1),Write(b1_text),GrowFromCenter(b2),Write(b2_text),GrowFromCenter(b3),Write(b3_text), run_time=2)

    b11 = Brace(VGroup(b1, b1_text, form[3], form[4]), UP)
    b21 = Brace(VGroup(b2, b2_text, form[6], form[7]), UP)
    b31 = Brace(VGroup(b3, b3_text, form[11], form[12]), UP)
    b11.align_to(b21, UP)
    b31.align_to(b21, UP)

    b11_text = b11.get_text(r"$\bot$")
    b11_text.set_color(RED)

    b21_text = b21.get_text(r"$\top$")
    b21_text.set_color(GREEN)

    b31_text = b31.get_text(r"$\top$")
    b31_text.set_color(GREEN)
    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text), run_time=2)

    q2 = TextMobject(r"When $x \in (x_1, x_2)$: ", r"$\top$")
    q2.set_color(GREEN)
    q2.move_to(UP)
    self.play(ReplacementTransform(q, q2))

    self.wait()

    self.play(FadeOut(b1),FadeOut(b1_text),FadeOut(b2),FadeOut(b2_text),FadeOut(b3),FadeOut(b3_text),FadeOut(b11),FadeOut(b11_text),FadeOut(b21),FadeOut(b21_text),FadeOut(b31),FadeOut(b31_text),FadeOut(q2))

    # 4
    q = TextMobject(r"When $x = x_2$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$0$")
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$+$")
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$0$")
    self.play(GrowFromCenter(b1),Write(b1_text),GrowFromCenter(b2),Write(b2_text),GrowFromCenter(b3),Write(b3_text), run_time=2)

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

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text), run_time=2)

    q2 = TextMobject(r"When $x = x_2$: ", r"$\top$")
    q2.set_color(GREEN)
    q2.move_to(UP)
    self.play(ReplacementTransform(q, q2))

    self.wait()

    self.play(FadeOut(b1),FadeOut(b1_text),FadeOut(b2),FadeOut(b2_text),FadeOut(b3),FadeOut(b3_text),FadeOut(b11),FadeOut(b11_text),FadeOut(b21),FadeOut(b21_text),FadeOut(b31),FadeOut(b31_text),FadeOut(q2))

    # 5
    q = TextMobject(r"When $x \in (x_2, \infty)$: ", r"?")
    q.move_to(UP)
    self.play(Write(q))

    b1 = Brace(form[3], UP)
    b1_text = b1.get_text("$+$")
    b2 = Brace(form[6], UP)
    b2_text = b2.get_text("$+$")
    b3 = Brace(form[11], UP)
    b3_text = b3.get_text("$-$")
    self.play(GrowFromCenter(b1),Write(b1_text),GrowFromCenter(b2),Write(b2_text),GrowFromCenter(b3),Write(b3_text), run_time=2)

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

    self.play(GrowFromCenter(b11),Write(b11_text),GrowFromCenter(b21),Write(b21_text),GrowFromCenter(b31),Write(b31_text), run_time=2)

    q2 = TextMobject(r"When $x \in (x_2, \infty)$: ", r"$\top$")
    q2.set_color(GREEN)
    q2.move_to(UP)
    self.play(ReplacementTransform(q, q2))

    self.wait()

    self.play(FadeOut(b1),FadeOut(b1_text),FadeOut(b2),FadeOut(b2_text),FadeOut(b3),FadeOut(b3_text),FadeOut(b11),FadeOut(b11_text),FadeOut(b21),FadeOut(b21_text),FadeOut(b31),FadeOut(b31_text),FadeOut(q2))

    form2 = TexMobject(r"\vDash", r"\forall x", r"\,[", r"(", r"p_1(x)", r"\geq 0", r"\,\wedge\,", r"p_2(x)", r"\geq 0", r")", r"\,\vee\,", r"(", r"p_3(x)", r"> 0", r")", "]")
    form2[0].set_color(GREEN)
    form2[4].set_color(BLUE)
    form2[7].set_color(YELLOW)
    form2[12].set_color(PURPLE)

    self.play(FadeOut(mat3),ApplyMethod(form.move_to, ORIGIN))
    self.wait()
    self.play(ReplacementTransform(form, form2))




    # mat2 = TexMobject(r"\begin{array}{cccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\ p_1 & + \\ p_2 & - \\ p_3 & 0 \end{array}")
    # mat2.move_to(2*DOWN)
    # self.play(ReplacementTransform(mat, mat2))


    self.wait()
    self.wait()

    # func_graph=self.get_graph(self.func_to_graph,self.function_color)
    # func_graph2=self.get_graph(self.func_to_graph2)
    # vert_line = self.get_vertical_line_to_graph(TAU,func_graph,color=YELLOW)
    # graph_lab = self.get_graph_label(func_graph, label = "\\cos(x)")
    # graph_lab2=self.get_graph_label(func_graph2,label = "\\sin(x)", x_val=-10, direction=UP/2)
    # two_pi = TexMobject("x = 2 \\pi")
    # label_coord = self.input_to_graph_point(TAU,func_graph)
    # two_pi.next_to(label_coord,RIGHT+UP)

    # self.play(ShowCreation(func_graph),ShowCreation(func_graph2))
    # self.play(ShowCreation(vert_line), ShowCreation(graph_lab), ShowCreation(graph_lab2),ShowCreation(two_pi))

  def p1(self,x):
    return 0.2 * x**2 - 0.2

  def p2(self,x):
    return 0.05 * (x + 1)**3
  
  def p3(self,x):
    return -0.25*x + 0.25
    
    
