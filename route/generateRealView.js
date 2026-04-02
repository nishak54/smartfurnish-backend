import express from "express";
import OpenAI from "openai";
import fs from "fs/promises";
import path from "path";

const router = express.Router();
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

router.post("/generate-real-view", async (req, res) => {
  try {
    const { roomType, budget, sofa, table } = req.body;

    const sofaPath = path.join(process.cwd(), "public", sofa.imagePath.replace(/^\/+/, ""));
    const tablePath = path.join(process.cwd(), "public", table.imagePath.replace(/^\/+/, ""));

    const [sofaBuffer, tableBuffer] = await Promise.all([
      fs.readFile(sofaPath),
      fs.readFile(tablePath),
    ]);

    const sofaBase64 = sofaBuffer.toString("base64");
    const tableBase64 = tableBuffer.toString("base64");

    const prompt = `
Create a photorealistic ${roomType} interior scene.
Use the provided sofa as the main seating furniture.
Use the provided center table in front of the sofa.
The final image should feel like a real professionally photographed living room.
Keep proportions realistic, elegant, warm, natural, balanced, and premium.
Budget target: $${budget}.
Style: modern realistic apartment.
Lighting: soft daylight.
Avoid cartoon, illustration, 3D render look, collage look, or cutout look.
`;

    const response = await openai.responses.create({
      model: "gpt-5",
      input: [
        {
          role: "user",
          content: [
            { type: "input_text", text: prompt },
            {
              type: "input_image",
              image_url: `data:image/webp;base64,${sofaBase64}`,
            },
            {
              type: "input_image",
              image_url: `data:image/webp;base64,${tableBase64}`,
            },
          ],
        },
      ],
      tools: [{ type: "image_generation" }],
    });

    const imageData = response.output.find(
      (item) => item.type === "image_generation_call"
    )?.result;

    if (!imageData) {
      return res.status(500).json({ error: "No image returned" });
    }

    res.json({ imageBase64: imageData });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to generate real view" });
  }
});

export default router;