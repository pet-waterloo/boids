###
#vertex
#version 300 es

in vec3 vvert;
in vec2 vuv;

out vec2 fuv;

uniform mat4 view, proj;
uniform mat4 model;
uniform mat4 scale;

void main(){
    gl_Position = proj * view * model * scale * vec4(vvert, 1.0);
    fuv = vuv;
}

###
#fragment
#version 300 es

in vec2 fuv;

out vec4 fragColor;

uniform float utime;
uniform sampler2D tex;

void main()
{
    // fragColor = texture(tex, fuv);
    fragColor = vec4(fuv, sin(utime), 1.0);
}


