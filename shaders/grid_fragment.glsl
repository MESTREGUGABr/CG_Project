#version 330 core

in vec3 FragPos;
out vec4 FragColor;

void main()
{
    // Simple grid pattern
    float gridSize = 0.5;
    vec2 coord = FragPos.xz / gridSize;
    vec2 grid = abs(fract(coord - 0.5) - 0.5) / fwidth(coord);
    float line = min(grid.x, grid.y);
    float alpha = 1.0 - min(line, 1.0);

    // Fade with distance
    float dist = length(FragPos.xz);
    float fade = 1.0 - smoothstep(3.0, 6.0, dist);

    vec3 color = vec3(0.35);
    FragColor = vec4(color, alpha * 0.5 * fade);
}
