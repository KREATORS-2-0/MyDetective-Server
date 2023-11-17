const axios = require("axios");

const openaiApiKey = "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"; // Load API key from environment variable

async function getCompletion(
  prompt,
  messages,
  model = "gpt-4",
  temperature = 0
) {
  messages.push({ role: "user", content: prompt });

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${openaiApiKey}`,
      },
      body: JSON.stringify({
        model: model,
        messages: messages,
        temperature: temperature,
      }),
    });

    const data = await response.json();

    messages.push({
      role: "assistant",
      content: data.choices[0].message.content,
    });

    return data.choices[0].message.content;
  } catch (e) {
    return `An error occurred: ${e}`;
  }
}

// Example usage
(async () => {
  let conversationHistory = [];

  const prompt1 = "Hi, my name is Taekwan. Nice to meet you!";
  let response = await getCompletion(prompt1, conversationHistory);
  console.log(response);

  const prompt2 = "Do you know my name?";
  response = await getCompletion(prompt2, conversationHistory);
  console.log(response);
})();
