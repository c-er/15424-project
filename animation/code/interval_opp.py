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
    mat = TexMobject(r"\begin{array}{cccccccc} & \dots & \dots & x_i & (x_{i}, x_{i + 1}) & x_{i + 1} & \dots & \dots \\ p_1' & \dots & \dots & - & - & - & \dots & \dots \\ p_2 & \dots & \dots & 0 & + & 0 & \dots & \dots \\ p_1 & \dots & \dots & + & ? & - & \dots & \dots \end{array}")
    mat.move_to(2 * DOWN)
    mat[0][62].set_color(YELLOW)
    mat[0][63].set_color(YELLOW)
    mat[0][70].set_color(YELLOW)
    mat[0][71].set_color(YELLOW)
    mat[0][72].set_color(YELLOW)

    self.play(Write(mat))

    self.setup_axes(animate=True)
    a = Dot().move_to(self.coords_to_point(0.5, 0))
    b = Dot().move_to(self.coords_to_point(2.5, 0))
    alab = TexMobject(r"x_i").next_to(a, DOWN)
    blab = TexMobject(r"x_{i + 1}").next_to(b, UP)

    self.play(ShowCreation(a), ShowCreation(b))
    self.play(Write(alab), Write(blab))

    p1a = Dot().move_to(self.coords_to_point(0.5, 0.5)).set_color(YELLOW)
    p1alab = TexMobject(r"p_1(x_i) > 0").next_to(p1a, UP).set_color(YELLOW)
    p1aline = DashedLine(p1a, a)
    p1b = Dot().move_to(self.coords_to_point(2.5, -0.5)).set_color(YELLOW)
    p1blab = TexMobject(r"p_1(x_{i + 1}) < 0").next_to(p1b, DOWN).set_color(YELLOW)
    p1bline = DashedLine(p1b, b)

    self.play(ReplacementTransform(mat[0][70].deepcopy(), VGroup(p1a, p1alab, p1aline)), run_time=1.5)
    self.play(ReplacementTransform(mat[0][72].deepcopy(), VGroup(p1b, p1blab, p1bline)), run_time=1.5)

    self.wait()

    conn = Line(p1a, p1b).set_color(YELLOW)
    c = Dot().move_to(self.coords_to_point(1.5, 0)).set_color(RED)
    clab = TexMobject(r"c").next_to(c, DOWN).set_color(RED)

    self.play(ShowCreation(conn))
    self.play(ShowCreation(c))
    self.play(Write(clab))
    self.wait()

    lc = VGroup(mat[0][6], mat[0][7])
    lc1 = mat[0][36].deepcopy()
    lc2 = mat[0][53].deepcopy()
    lc3 = mat[0][70].deepcopy()
    mc = VGroup(*list(mat[0][i] for i in range(8, 17)))
    rc = VGroup(mat[0][17], mat[0][18], mat[0][19], mat[0][20])
    rc1 = mat[0][38].deepcopy()
    rc2 = mat[0][55].deepcopy()
    rc3 = mat[0][72].deepcopy()

    l = [(VGroup(mat[0][6], mat[0][7]), mat[0][1]), (mat[0][36], mat[0][31]), (mat[0][53], mat[0][48]), (mat[0][70], mat[0][65])]
    fo = [mat[0][i] for i in range(0, 6)] + ([mat[0][i] for i in range(30, 36)]) + ([mat[0][i] for i in range(47, 53)]) + ([mat[0][i] for i in range(64, 70)])
    l2 = [(VGroup(mat[0][17], mat[0][18], mat[0][19], mat[0][20]), mat[0][25]), (mat[0][38], mat[0][43]), (mat[0][55], mat[0][60]), (mat[0][72], mat[0][77])]
    fo2 = [mat[0][i] for i in range(21, 27)] + ([mat[0][i] for i in range(39, 45)]) + ([mat[0][i] for i in range(56, 62)]) + ([mat[0][i] for i in range(73, 79)])
    fo3 = VGroup(*list(mat[0][i] for i in range(8, 17)))
    anims = []
    for i in l:
      anims.append(ApplyMethod(i[0].move_to, i[1]))
    
    for i in l2:
      anims.append(ApplyMethod(i[0].move_to, i[1]))
    
    for i in fo:
      anims.append(FadeOut(i))
    
    for i in fo2:
      anims.append(FadeOut(i))
    
    lcn = TexMobject(r"(x_i, c)").move_to(lc)
    rcn = TexMobject(r"(c, x_{i + 1})").move_to(rc)
    lcn[0][4].set_color(RED)
    rcn[0][1].set_color(RED)
    
    cc = clab.deepcopy()
    self.play(*anims)
    self.play(FadeOut(fo3))
    self.play(ApplyMethod(cc.move_to, mc), ReplacementTransform(clab.deepcopy(), lcn), (ReplacementTransform(clab.deepcopy(), rcn)))

    self.wait(2)

    self.play(ApplyMethod(mat[0][37].deepcopy().move_to, lc1), ApplyMethod(mat[0][37].deepcopy().move_to, rc1))
    self.wait()
    self.play(ApplyMethod(mat[0][54].deepcopy().move_to, lc2), ApplyMethod(mat[0][54].deepcopy().move_to, rc2))
    self.wait()

    zero = TexMobject(r"0").move_to(mat[0][71]).set_color(YELLOW)
    
    self.play(ApplyMethod(mat[0][70].deepcopy().move_to, lc3), run_time=1.5)
    self.wait()
    self.play(FadeOut(mat[0][71]), ReplacementTransform(c.deepcopy(), zero), run_time=1.5)
    self.wait()
    self.play(ApplyMethod(mat[0][72].deepcopy().move_to, rc3), run_time=1.5)
    self.wait()


    self.wait(3)