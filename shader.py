import OpenGL.GL as gl
import OpenGL.GL.shaders as sh


class Shader:
    def __init__(self, vs, fs):
        self.handles = {}
        self._id = sh.compileProgram(
            self.get_shader(vs, gl.GL_VERTEX_SHADER),
            self.get_shader(fs, gl.GL_FRAGMENT_SHADER),)

    @staticmethod
    def get_shader(src, shader_type):
        with open(src) as file:
            src_text = file.read()
        return sh.compileShader(src_text, shader_type)

    def get_id(self):
        return self._id

    def bind(self):
        gl.glUseProgram(self._id)

    @staticmethod
    def unbind():
        gl.glUseProgram(0)

    def save_attr_locations(self, attrs):
        for attr in attrs:
            self.handles[attr] = gl.glGetAttribLocation(self._id, attr)

    def save_uniform_locations(self, uniforms):
        for uniform in uniforms:
            self.handles[uniform] = gl.glGetUniformLocation(self._id, uniform)
