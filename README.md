# VHDL Code Generator Pro

A modern, PyQt5-based GUI application that allows users to quickly generate VHDL code for common digital design components such as multiplexers, decoders, encoders, demultiplexers, shift registers, SRAM, and clock dividers. Includes syntax highlighting, code export options, and PDF generation.

---

## ✨ Features

* **Graphical Interface**: Built with PyQt5, offers a sleek and responsive GUI.
* **VHDL Syntax Highlighting**: Real-time syntax highlighting for better code visibility.
* **Component Generator Tabs**: Generate VHDL for:

  * MUX
  * Decoder
  * Encoder
  * Demux
  * Shift Register (SIPO/PISO)
  * SRAM
  * Clock Divider
* **Dark Mode UI**: Clean and modern interface with dark theme.
* **Code Exporting**:

  * Copy to clipboard
  * Save to `.vhdl`
  * Export to PDF
* **Customizable Parameters**: Easily adjust component-specific attributes such as bit width, input lines, memory depth, etc.

---

## 📦 Requirements

* Python 3.7+
* PyQt5
* fpdf
* pyperclip

Install dependencies via:

```bash
pip install PyQt5 fpdf pyperclip
```

---

## 🚀 How to Run

```bash
python vhdl_generator.py
```

---

## 🛠 Usage

1. Enter **project**, **entity**, and **architecture** names.
2. Select the **component tab** (e.g., MUX, Decoder).
3. Customize settings (e.g., number of inputs, address bits).
4. Click **Generate** to preview code.
5. Use **Copy**, **Save**, or **Export PDF** to output the result.

---

## 📄 Example

**Generated MUX Code Sample**:

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity my_mux is
    Port(
        inputs : in STD_LOGIC_VECTOR(3 downto 0);
        sel    : in STD_LOGIC_VECTOR(1 downto 0);
        output : out STD_LOGIC
    );
end my_mux;

architecture behavioral of my_mux is
begin
    process(sel, inputs)
    begin
        case sel is
            when "00" => output <= inputs(0);
            when "01" => output <= inputs(1);
            when "10" => output <= inputs(2);
            when "11" => output <= inputs(3);
            when others => output <= '0';
        end case;
    end process;
end behavioral;
```

---

## 📌 Notes

* VHDL code is compatible with standard simulators and FPGA design tools.
* More components and customization options coming soon!

---

## 📃 License

MIT License
