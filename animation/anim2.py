from manimlib.imports import *

class Test(Scene):
  CUSTOM_CONFIG = {
        "v_buff": 0.8,
        "h_buff": 1.3,
        "bracket_h_buff": MED_SMALL_BUFF,
        "bracket_v_buff": MED_SMALL_BUFF,
        "add_background_rectangles_to_entries": False,
        "include_background_rectangle": False,
        "element_to_mobject": TexMobject,
        "element_to_mobject_config": {},
        "element_alignment_corner": UL,
        "left_bracket": "",
        "right_bracket": "",
    }
  Matrix.CONFIG = CUSTOM_CONFIG
  def construct(self):
    mat = Matrix([[r"\cdot", "", r"(-\infty, x_1)", "x_1", "", r"(x_1, x_2)", "x_2", "", r"(x_2, \infty)"],
                  [r"p_1", "", "?", "?", "", "?", "?", "", "?"]])
    # mat = TexMobject(r"\begin{array}{cccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\ p_1 \\ p_2 \\ p_3 \end{array}")
    

    self.play(ShowCreation(mat))

    self.wait()