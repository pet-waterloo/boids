###
#vertex
#version 300 es

in vec3 vvert;
in vec2 vuv;
in vec3 vnorm;

uniform mat4 view;
uniform mat4 proj;
uniform mat4 model;
uniform mat4 scale;

out vec2 fuv;
out vec3 fnorm;

void main() {
    gl_Position = proj * view * model * scale * vec4(vvert, 1.0);
    fuv = vuv;
    fnorm = vnorm;
}

###
#fragment
#version 300 es
precision mediump float;

in vec2 fuv;
in vec3 fnorm;

uniform sampler2D tex;

out vec4 fragColor;


void main() {
    vec3 norm = normalize(fnorm);
    vec3 light = normalize(vec3(0.0, 0.0, 1.0));
    float diff = max(dot(norm, light), 0.0);
    vec4 v = texture(tex, fuv);
    vec3 color = v.rgb;
    // fragColor = vec4(color * diff, 1.0);
    fragColor = v;
}

