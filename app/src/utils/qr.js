import QRCode from "qrcode";

export const generateQR = async (text) => {
  try {
    return await QRCode.toDataURL(text, {
      width: 128,
      margin: 0,
      color: {
        dark: "#0E0D0D",
        light: "#ffffff00",
      },
    });
  } catch (err) {
    console.error(err);
  }
};