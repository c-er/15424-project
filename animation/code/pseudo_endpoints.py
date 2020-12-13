from manimlib.imports import *
import os
import pyclbr
class PlotFunctions(GraphScene):
  CONFIG = {
    "x_min" : -0.25,
    "x_max" : 3,
    "y_min" : -0.5,
    "y_max" : 2,
    "graph_origin" : 2 * UP + 4*LEFT ,
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
    # axes = Axes(x_min=-2, x_max=2, y_min=-1.2, y_max=2, color=GREEN)
    self.setup_axes(animate=True)
    xn = Dot().move_to(self.coords_to_point(2,0))
    xn_lab = TexMobject(r"x_n").next_to(xn, DOWN)

    self.play(ShowCreation(xn))
    self.play(Write(xn_lab))

    gp1 = self.get_graph(self.p1,color=PURPLE, x_min=2, x_max=3)
    gp1_lab = self.get_graph_label(gp1, label=r"p_1'", x_val=2, direction=LEFT)
    gp1_lab.set_color(PURPLE)
    gp2 = self.get_graph(self.p2, color=YELLOW, x_min=2, x_max=3)
    gp2_lab = self.get_graph_label(gp2, label=r"p_1", x_val=2, direction=1.5 * UP)
    gp2_lab.set_color(YELLOW)

    mat = TexMobject(r"\begin{array}{ccc} & \dots & (x_n, \infty) \\ p_1' & \ddots & + \\ \vdots & \vdots & \vdots \end{array}")
    mat.move_to(2*DOWN)
    mat[0][9].set_color(PURPLE)
    mat[0][10].set_color(PURPLE)
    mat[0][11].set_color(PURPLE)
    mat[0][15].set_color(PURPLE)
    self.play(Write(mat))

    self.wait()

    dc = mat[0][15].deepcopy()
    self.play(ReplacementTransform(dc, gp1))
    self.play(Write(gp1_lab))
    self.wait()

    self.play(ShowCreation(gp2))
    self.play(Write(gp2_lab))
    self.wait()

    stmt = TextMobject(r"$p_1(\infty)$ is $+$")
    stmt.set_color(YELLOW)
    self.play(ReplacementTransform(VGroup(gp2, gp2_lab), stmt))

    self.wait(2)

    self.play(*list(map(lambda x: FadeOut(x), [mat, gp1, gp1_lab, stmt, xn, xn_lab, self.axes])))

    self.CONFIG["x_min"] = -3
    self.x_min = -3
    self.CONFIG["x_max"] = 0.25
    self.x_max = 0.25
    self.CONFIG["graph_origin"] = 2 * DOWN + 4 * RIGHT
    self.graph_origin = 2 * UP + 4 * RIGHT

    self.setup_axes(animate=True)

    self.wait()

    x1 = Dot().move_to(self.coords_to_point(-2,0))
    x1_lab = TexMobject(r"x_1").next_to(x1, DOWN)

    self.play(ShowCreation(x1))
    self.play(Write(x1_lab))

    mat = TexMobject(r"\begin{array}{ccc} & (-\infty, x_1) & \dots \\ p_1' & + & \dots \\ \vdots & \vdots & \ddots \end{array}")
    mat.move_to(2*DOWN)
    mat[0][10].set_color(PURPLE)
    mat[0][11].set_color(PURPLE)
    mat[0][12].set_color(PURPLE)
    mat[0][13].set_color(PURPLE)
    self.play(Write(mat))
    self.wait()

    gp1 = self.get_graph(self.np1,color=PURPLE, x_min=-3, x_max=-2)
    gp1_lab = self.get_graph_label(gp1, label=r"p_1'", direction=LEFT, x_val=-3)
    gp1_lab.set_color(PURPLE)
    gp2 = self.get_graph(self.np2, color=YELLOW, x_min=-3, x_max=-2)
    gp2_lab = self.get_graph_label(gp2, label=r"p_1", direction=LEFT, x_val=-3)
    gp2_lab.set_color(YELLOW)

    dc = mat[0][13].deepcopy()
    self.play(ReplacementTransform(dc, gp1))
    self.play(Write(gp1_lab))
    self.wait()

    self.play(ShowCreation(gp2))
    self.play(Write(gp2_lab))
    self.wait()

    stmt = TextMobject(r"$p_1(-\infty)$ is $-$")
    stmt.set_color(YELLOW)
    self.play(ReplacementTransform(VGroup(gp2, gp2_lab), stmt))

    self.wait(2)

  
  def p1(self, x):
    return 0.3*x - 0.3
  
  def p2(self, x):
    return 0.15*(x**2) - 0.3*x + 0.45
  
  def np1(self, x):
    return 0.3*(-x) - 0.3
  
  def np2(self, x):
    return -0.15*(x**2) - 0.3*(x) - 0.5