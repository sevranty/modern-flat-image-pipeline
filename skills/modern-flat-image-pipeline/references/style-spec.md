# Modern Flat style contract

```yaml
style_id: modern-flat
style_version: 0.1.0
status: draft
```

## 1. Canonical definition

Modern Flat is a detailed, vector-like illustration system built from structured planar geometry, volumetric gradient modeling, one coherent directional lighting system, clean layered shadows, controlled rim light, and atmospheric depth.

The result must feel dimensional and polished without becoming photographic, painterly, or glossy 3D CGI.

## 2. Style invariants

A valid Modern Flat image must satisfy all of the following families.

### 2.1 Geometry

- Use clean, structured planar or semi-planar shapes.
- Preserve a readable silhouette at thumbnail size.
- Simplify real-world forms without losing identity or function.
- Model volume through shape transitions, tonal planes, gradients, overlap, and shadow.
- Keep edges deliberate and free from texture noise.
- Concentrate detail in the focal area; reduce detail in supporting regions.

### 2.2 Light

- Use one dominant directional key light.
- Keep highlight and shadow direction consistent across all objects.
- Use controlled rim light only where it improves silhouette, separation, or hierarchy.
- Avoid random highlights, conflicting light sources, and physically unexplained glow.
- Make light clarify form rather than imitate a photographic studio render.

### 2.3 Volume and depth

- Use volumetric gradients inside important shapes.
- Use clean layered cast and contact shadows.
- Separate foreground, midground, and background.
- Use overlap and scale to communicate depth.
- Use atmospheric depth by reducing contrast, saturation, or detail in distant layers.
- Avoid flat icon-like treatment with no depth unless the scene brief explicitly requests an intentionally simplified derivative.

### 2.4 Composition

- Establish one obvious visual center.
- Make the main subject readable first.
- Use secondary elements to support the action, meaning, or spatial context.
- Preserve controlled negative space when required by the output use.
- Create a clear reading path through scale, direction, overlap, contrast, and accent placement.
- Keep critical content compatible with the declared crop and safe-area rules.

### 2.5 Surface treatment

- Use clean vector-like surfaces.
- Prefer tonal modeling over simulated physical material realism.
- Keep microtexture minimal or absent.
- Do not use grunge, film grain, canvas, watercolor paper, brushed paint, or photographic noise as default surface language.

### 2.6 Detail

- The image may be highly detailed, but detail must be hierarchical.
- The focal subject may contain more internal structure, smaller shapes, and stronger tonal separation.
- Background detail must remain subordinate.
- Decorative detail that does not support meaning, identity, or depth is a defect.

## 3. Controlled variables

The following may change without changing the style identity:

- subject and story;
- environment;
- mood;
- time of day;
- camera angle;
- aspect ratio;
- dominant palette family;
- saturation;
- number of objects;
- degree of abstraction;
- depth intensity;
- level of focal detail;
- background complexity.

A variable becomes locked only when the Scene Brief, Reference Map, or explicit user instruction requires it.

## 4. Role-based palette

Modern Flat has no fixed corporate palette. Build each scene from color roles.

| Role | Typical visual share | Purpose |
|---|---:|---|
| Neutral base | 35-55% | background, large surfaces, breathing room |
| Dominant group | 25-40% | scene identity and main color family |
| Supporting group | 10-20% | depth, separation, secondary information |
| Focal accent | 5-15% | visual center, action, or critical signal |

Rules:

- Use the focal accent intentionally, not uniformly.
- Preserve focal contrast at thumbnail size.
- Do not let every object compete at equal saturation or contrast.
- Palette direction may come from the task or an explicitly assigned reference role, but it cannot override the style invariants.
- If a reference palette causes photographic or painterly drift, translate its relationships rather than copying its exact rendering behavior.

## 5. Character and object treatment

### People

- Preserve a clear gesture, pose, age range, and role when required.
- Simplify anatomy without breaking joints, hands, facial structure, or body logic.
- Use facial detail appropriate to output size.
- Do not introduce unverified sensitive attributes.

### Products, machines, and architecture

- Preserve identity-defining structure under Identity Lock.
- Simplify surface detail while retaining function and recognizable construction.
- Do not invent impossible connections, duplicated parts, or nonfunctional geometry.

### Abstract metaphors

- Keep the metaphor readable in two to three seconds.
- Use a clear object-action relationship.
- Avoid symbolic clutter that requires explanatory text.

## 6. Background and spatial system

A Modern Flat background is functional, not wallpaper.

It may:

- establish location;
- create depth;
- frame the subject;
- support direction or movement;
- reserve negative space;
- explain scale or mechanism.

It must not:

- overpower the subject;
- introduce unrelated narrative elements;
- become a photographic environment behind flat foreground objects;
- use ambient decoration with no semantic or spatial function.

## 7. Anti-drift boundaries

### Modern Flat vs generic flat

Modern Flat includes dimensional gradient modeling, coherent light, layered shadows, and spatial depth. Generic flat without depth fails the contract.

### Modern Flat vs glossy 3D CGI

Modern Flat uses planar, vector-like modeling. It does not depend on physically simulated plastic, chrome, ray-traced reflection, or glossy render materials.

### Modern Flat vs photorealism

Modern Flat simplifies form and surface. It does not imitate lens behavior, skin pores, realistic material microtexture, photographic bokeh, or camera noise.

### Modern Flat vs painterly illustration

Modern Flat uses clean shape construction and controlled gradients. It does not use visible brushwork, watercolor bleeding, canvas texture, or expressive paint as the primary rendering language.

### Modern Flat vs anime or fantasy styling

Modern Flat may depict fictional subjects, but it does not inherit anime facial conventions, fantasy costume language, magical glow, or genre rendering unless explicitly requested as content and still compatible with the core style.

## 8. Forbidden markers

Reject or correct output dominated by:

- photorealism or hyperrealism;
- photographic texture or lens simulation;
- painterly, watercolor, oil, charcoal, or grunge surfaces;
- glossy plastic CGI;
- chrome or mirror-like reflection;
- ray-traced reflections as a defining effect;
- photographic bokeh or shallow depth of field;
- random glow, bloom, sparks, or decorative particles;
- generic flat minimalism without dimensional modeling;
- inconsistent light direction;
- dirty texture noise;
- random text;
- watermarks;
- unrequested logos;
- direct imitation of a named living artist.

## 9. Positive prompt markers

A generator-facing prompt should express these concepts when relevant:

- detailed dimensional Modern Flat illustration;
- clean structured planar geometry;
- readable silhouette;
- vector-like surfaces;
- volumetric gradient modeling;
- clean layered shadows;
- one consistent directional key light;
- controlled rim light;
- foreground, midground, and background separation;
- atmospheric depth;
- polished but explicitly non-photorealistic.

Do not require exact wording. Validate semantic coverage, not string identity.

## 10. Style acceptance test

A candidate passes the style gate only when:

1. the silhouette and main action are readable;
2. the geometry is clean and planar or vector-like;
3. volume comes from gradients, tonal planes, overlap, and shadows;
4. one coherent light direction is visible;
5. depth layers are present when the scene requires spatial context;
6. detail is hierarchical;
7. the result is clearly non-photorealistic;
8. none of the critical forbidden markers dominate the image.

If any critical style defect is present, the candidate cannot be accepted by score alone.
