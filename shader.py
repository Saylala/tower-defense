import OpenGL.GL as gl
import OpenGL.GL.shaders as sh


class Shader:
    def __init__(self, vs, fs):
        self.handles = {}
        self._id = sh.compileProgram(self.get_shader(vs, gl.GL_VERTEX_SHADER),
                                  self.get_shader(fs, gl.GL_FRAGMENT_SHADER),)

    @staticmethod
    def get_shader(src, shader_type):
        with open(src) as f:
            src_text = f.read()
        return sh.compileShader(src_text, shader_type)

    def get_id(self):
        return self._id

    def bind(self):
        gl.glUseProgram(self._id)

    @staticmethod
    def unbind():
        gl.glUseProgram(0)

    def save_attr_locations(self, attrs):
        for e in attrs:
            self.handles[e] = gl.glGetAttribLocation(self._id, e)

    def save_uniform_locations(self, uniforms):
        for e in uniforms:
            self.handles[e] = gl.glGetUniformLocation(self._id, e)
