from manimlib.imports import *
import os
import pyclbr
class PlotFunctions(GraphScene):
  CONFIG = {
    "x_min" : -0.25,
    "x_max" : 3,
    "y_min" : -0.75,
    "y_max" : 0.75,
    "graph_origin" : 4 * LEFT,
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
    self.setup_axes(animate=True)

    a = Dot().move_to(self.coords_to_point(0.5,0))
    a_lab = TexMobject(r"a")
    a_lab.next_to(a, DOWN)
    b = Dot().move_to(self.coords_to_point(2.5, 0))
    b_lab = TexMobject(r"b")
    b_lab.next_to(b, DOWN)

    self.play(ShowCreation(a), ShowCreation(b))
    self.play(Write(a_lab), Write(b_lab))
    
    x1 = Dot().move_to(self.coords_to_point(1,0))
    x1_lab = TexMobject(r"x_1").next_to(x1,DOWN)
    x2 = Dot().move_to(self.coords_to_point(2, 0))
    x2_lab = TexMobject(r"x_2").next_to(x2,DOWN)

    p1 = self.get_graph(self.p1,color=YELLOW, x_min=0.5, x_max=2.5)
    p1_lab = self.get_graph_label(p1, label=r"p_1")
    p1_lab.set_color(YELLOW)
    p1p = self.get_graph(self.deriv, color=BLUE)
    p1p.set_opacity(0.35)
    p1p_lab = self.get_graph_label(p1p, label=r"p_1'", direction=1.7*LEFT)
    p1p_lab.set_color(BLUE)


    self.play(ShowCreation(p1), run_time=2)
    self.play(Write(p1_lab))

    self.play(ShowCreation(x1), ShowCreation(x2))
    self.play(Write(x1_lab), Write(x2_lab))

    self.wait()

    ss_group = self.get_secant_slope_group(0.75, p1, dx=0.0001, secant_line_color=PURPLE)

    self.play(*list(map(ShowCreation, ss_group)))

    self.animate_secant_slope_group_change(ss_group, target_x=1.5, run_time=4)

    line = DashedLine(self.coords_to_point(1.5,-0.5), self.coords_to_point(1.5,0))
    self.play(ShowCreation(line), run_time=2)

    pt = Dot().move_to(self.coords_to_point(1.5,-0.5)).set_color(WHITE)
    droot = Dot().move_to(self.coords_to_point(1.5,0)).set_color(RED)
    droot_lab = TextMobject(r"Root of $p_1'$").set_color(RED).next_to(droot,UP)
    tan_lab = TextMobject(r"Tangent slope is $0$").next_to(pt, 0.75*DOWN)
    self.play(ShowCreation(droot), ShowCreation(pt))
    self.wait()
    self.play(ReplacementTransform(pt.deepcopy(), tan_lab), run_time=1.5)
    self.wait()
    self.wait()
    self.play(ReplacementTransform(droot.deepcopy(), droot_lab), run_time=1.5)


    self.wait(3)

  def p1(self, x):
    return 2*(x - 1.5)**2 - 0.5
  
  def deriv(self, x):
    return 4*(x - 1.5)