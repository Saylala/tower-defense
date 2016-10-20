import ctypes
from array import array

import OpenGL.GL as gl


class Mesh:
    def __init__(self, vertices, indices, uvs):
        self._vertex_buffer = self.create_buffer(
            vertices, 3, 'f', gl.GL_ARRAY_BUFFER)
        self._uv_buffer = self.create_buffer(
            uvs, 2, 'f', gl.GL_ARRAY_BUFFER)
        self._index_buffer = self.create_buffer(
            indices, 1, 'H', gl.GL_ELEMENT_ARRAY_BUFFER)

        self._texture_id = -1

    def set_texture(self, img):
        image = img.convert("RGBA").tobytes("raw", "RGBA", 0, 1)

        self._texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture_id)

        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, 3,
                        img.size[0], img.size[1], 0,
                        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image)

    @staticmethod
    def create_buffer(arr, stride, array_type, buffer_type):
        result = {'count': 0}
        if arr:
            result['count'] = len(arr)//stride
            result['id'] = gl.glGenBuffers(1)
            gl.glBindBuffer(buffer_type, result['id'])
            gl.glBufferData(buffer_type,
                            array(array_type, arr).tobytes(),
                            gl.GL_STATIC_DRAW)
        return result

    def draw(self, handles):
        if handles["aVertexPosition"] != -1:
            if self._vertex_buffer['count'] != 0:
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_buffer['id'])
                gl.glEnableVertexAttribArray(handles["aVertexPosition"])
                gl.glVertexAttribPointer(handles["aVertexPosition"], 3,
                                         gl.GL_FLOAT, False,
                                         0, ctypes.c_void_p(0))

        if handles["aVertexTexCoord"] != -1:
            if self._uv_buffer['count'] != 0:
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._uv_buffer['id'])
                gl.glEnableVertexAttribArray(handles["aVertexTexCoord"])
                gl.glVertexAttribPointer(handles["aVertexTexCoord"], 2,
                                         gl.GL_FLOAT, False,
                                         0, ctypes.c_void_p(0))

        if handles["uTexture"] != -1:
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture_id)
            gl.glUniform1i(handles["uTexture"], 0)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_buffer['id'])
        gl.glDrawElements(gl.GL_TRIANGLES, self._index_buffer['count'],
                          gl.GL_UNSIGNED_SHORT, ctypes.c_void_p(0))

        gl.glDisableVertexAttribArray(handles["aVertexPosition"])

    @staticmethod
    def get_quad(x1, y1, x2, y2, z):
        vertices = [x2, y2, z,
                    x1, y2, z,
                    x2, y1, z,
                    x1, y1, z]
        uvs = [1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0]
        indices = [0, 1, 2, 1, 3, 2]
        return Mesh(vertices, indices, uvs)

    @staticmethod
    def get_line(point1, point2, priority, width, height):
        bias = 0.4
        x11 = -1 + (point1.col + bias) * width
        y11 = 1 - (point1.row + bias) * height
        x21 = -1 + (point2.col + bias) * width
        y21 = 1 - (point2.row + bias) * height

        bias = 0.6
        x12 = -1 + (point1.col + bias) * width
        y12 = 1 - (point1.row + bias) * height
        x22 = -1 + (point2.col + bias) * width
        y22 = 1 - (point2.row + bias) * height

        vertices = [x11, y11, priority,
                    x12, y12, priority,
                    x21, y21, priority,
                    x22, y22, priority]
        uvs = [1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0]
        indices = [0, 1, 2, 1, 3, 2]
        return Mesh(vertices, indices, uvs)
