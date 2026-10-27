// Avisos por email al dueño de la escuela (Cloudflare Email Routing, gratis).
// Envía desde avisos@bocetoo.app a la dirección verificada configurada en wrangler.toml ([[send_email]] AVISOS).
// Si algo falla, no corta la operación del alumno: solo queda en los registros del Worker.

const DESDE = "avisos@bocetoo.app";

const b64 = (s: string) => {
  const bytes = new TextEncoder().encode(s);
  let bin = ""; bytes.forEach((b) => { bin += String.fromCharCode(b); });
  return btoa(bin);
};

export async function avisar(env: any, asunto: string, texto: string): Promise<void> {
  const destino = env.AVISOS_PARA || "bnvds.nico@gmail.com";
  if (!env.AVISOS) { console.log("aviso (sin envío configurado):", asunto); return; }
  try {
    const { EmailMessage } = await import("cloudflare:email" as any);
    const id = `<${crypto.randomUUID()}@bocetoo.app>`;
    const cuerpo = b64(texto + "\n\n—\nAviso automático de bocetoo.app").replace(/.{1,76}/g, "$&\r\n");
    const raw = [
      `From: boceto avisos <${DESDE}>`,
      `To: ${destino}`,
      `Subject: =?UTF-8?B?${b64(asunto)}?=`,
      `Message-ID: ${id}`,
      `Date: ${new Date().toUTCString()}`,
      "MIME-Version: 1.0",
      "Content-Type: text/plain; charset=UTF-8",
      "Content-Transfer-Encoding: base64",
      "",
      cuerpo
    ].join("\r\n");
    await env.AVISOS.send(new EmailMessage(DESDE, destino, raw));
  } catch (e) {
    console.error("aviso: no se pudo enviar", asunto, String(e));
  }
}
