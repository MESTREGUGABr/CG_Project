#version 330 core

#define MAX_LIGHTS 10

struct Light {
    int type;       // 0 = directional (sun), 1 = point/spotlight
    vec3 position;
    vec3 direction;
    vec3 color;
    float intensity;
    float cutoff;       // for spotlight cone (cosine of angle)
    float outerCutoff;
};

uniform int numLights;
uniform Light lights[MAX_LIGHTS];
uniform vec3 viewPos;
uniform vec3 objectColor;
uniform float ambientStrength;

in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

vec3 calcDirectionalLight(Light light, vec3 normal, vec3 viewDir)
{
    vec3 lightDir = normalize(-light.direction);
    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0);
    // Specular (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 64.0);

    vec3 diffuse = diff * light.color * light.intensity;
    vec3 specular = spec * light.color * light.intensity * 0.5;
    return diffuse + specular;
}

vec3 calcPointLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir)
{
    vec3 lightDir = normalize(light.position - fragPos);
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (1.0 + 0.09 * distance + 0.032 * distance * distance);

    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0);
    // Specular (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 64.0);

    // Spotlight cone
    float intensity = light.intensity;
    if (light.cutoff > 0.0) {
        float theta = dot(lightDir, normalize(-light.direction));
        float epsilon = light.cutoff - light.outerCutoff;
        intensity *= clamp((theta - light.outerCutoff) / epsilon, 0.0, 1.0);
    }

    vec3 diffuse = diff * light.color * intensity * attenuation;
    vec3 specular = spec * light.color * intensity * attenuation * 0.5;
    return diffuse + specular;
}

void main()
{
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);

    // Ambient
    vec3 ambient = ambientStrength * vec3(1.0);

    // Accumulate light contributions
    vec3 result = ambient;
    for (int i = 0; i < numLights && i < MAX_LIGHTS; i++) {
        if (lights[i].type == 0) {
            result += calcDirectionalLight(lights[i], norm, viewDir);
        } else {
            result += calcPointLight(lights[i], norm, FragPos, viewDir);
        }
    }

    result *= objectColor;
    FragColor = vec4(result, 1.0);
}
