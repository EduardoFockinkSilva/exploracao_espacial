from OpenGL.GL import *

def configurar_luz() -> None:
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    intensidade_luz_global = 1.0
    luz_ambiente_global = [intensidade_luz_global, intensidade_luz_global, intensidade_luz_global*0.8, 1.0]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente_global)

    luz_difusa = [1.0, 1.0, 0.8, 1.0]
    luz_especular = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)

def definir_posicao_luz(posicao: list[float]) -> None:
    luz_posicao = [posicao[0], posicao[1], posicao[2], 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, luz_posicao)

def aplicar_material(emissivo: bool, cor: list[float]) -> None:
    if emissivo:
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, cor)
    else:
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, cor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)
