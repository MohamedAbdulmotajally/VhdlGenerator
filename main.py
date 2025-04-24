import sys
import pyperclip
from fpdf import FPDF
from PyQt5.QtCore import Qt, QRegExp, QSize
from PyQt5.QtGui import (QFont, QColor, QPalette, QIcon, QSyntaxHighlighter,
                         QTextCharFormat, QTextCursor)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QComboBox,
                             QTextEdit, QSpinBox, QGroupBox, QFormLayout,
                             QFileDialog, QMessageBox, QStatusBar, QMenuBar,
                             QAction, QTabWidget, QLineEdit, QToolButton,
                             QSizePolicy, QSpacerItem)

class VHDLHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for VHDL code"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []
        
        # Keywords
        keywords = [
            'entity', 'architecture', 'begin', 'end', 'process', 'port',
            'signal', 'variable', 'constant', 'generic', 'if', 'then',
            'else', 'case', 'when', 'others', 'library', 'use', 'downto'
        ]
        kw_format = QTextCharFormat()
        kw_format.setForeground(QColor("#C586C0"))
        kw_format.setFontWeight(QFont.Bold)
        for kw in keywords:
            pattern = QRegExp(r"\b" + kw + r"\b", Qt.CaseInsensitive)
            self.rules.append((pattern, kw_format))

        # Types
        types = ['std_logic', 'std_logic_vector', 'integer', 'natural', 'positive']
        type_format = QTextCharFormat()
        type_format.setForeground(QColor("#4EC9B0"))
        for t in types:
            pattern = QRegExp(r"\b" + t + r"\b", Qt.CaseInsensitive)
            self.rules.append((pattern, type_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.rules.append((QRegExp(r"--[^\n]*"), comment_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#D69D85"))
        self.rules.append((QRegExp(r'".*"'), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)

class VHDLGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VHDL Code Generator Pro")
        self.setGeometry(200, 100, 1000, 800)
        self.setWindowIcon(QIcon("icon.png"))
        self.dark_mode = True
        self.init_ui()
        self.apply_theme()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def init_ui(self):
        self.create_menu()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        main_layout = QVBoxLayout(self.central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # Project Configuration
        config_group = QGroupBox("Project Configuration")
        config_layout = QFormLayout()
        
        self.project_name = self.create_input("Project Name")
        self.entity_name = self.create_input("Entity Name")
        self.architecture_name = self.create_input("Architecture Name")
        
        self.proc_type = QComboBox()
        self.proc_type.addItems(["Process", "Function"])
        
        config_layout.addRow(QLabel("Project Name:"), self.project_name)
        config_layout.addRow(QLabel("Entity Name:"), self.entity_name)
        config_layout.addRow(QLabel("Architecture Name:"), self.architecture_name)
        config_layout.addRow(QLabel("Implementation Type:"), self.proc_type)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)

        # Component Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        
        components = [
            ("MUX", self.create_mux_tab()),
            ("Decoder", self.create_decoder_tab()),
            ("Encoder", self.create_encoder_tab()),
            ("Demux", self.create_demux_tab()),
            ("Shift Register", self.create_shift_register_tab()),
            ("SRAM", self.create_sram_tab()),
            ("Clock Divider", self.create_clock_divider_tab())
        ]

        for name, widget in components:
            self.tabs.addTab(widget, name)

        main_layout.addWidget(self.tabs)

        # Code Editor
        code_group = QGroupBox("Generated VHDL Code")
        code_layout = QVBoxLayout()
        self.code_display = QTextEdit()
        self.code_display.setFont(QFont("Consolas", 11))
        self.highlighter = VHDLHighlighter(self.code_display.document())
        code_layout.addWidget(self.code_display)
        code_group.setLayout(code_layout)
        main_layout.addWidget(code_group)

        # Action Buttons
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        actions = [
            ("Generate", "#569CD6", self.generate_code),
            ("Copy", "#DCDCAA", self.copy_code),
            ("Save", "#6A9955", self.save_code),
            ("Export PDF", "#C586C0", self.export_pdf)
        ]

        for text, color, func in actions:
            btn = QPushButton(text)
            btn.clicked.connect(func)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    color: {'black' if color == "#DCDCAA" else 'white'};
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ opacity: 0.9; }}
            """)
            btn_layout.addWidget(btn)

        main_layout.addWidget(btn_container)

    def create_input(self, placeholder):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #444;
                border-radius: 4px;
                background: #2d2d2d;
                color: white;
            }
        """)
        return input_field

    def create_mux_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        self.mux_inputs = QSpinBox()
        self.mux_inputs.setRange(2, 16)
        self.mux_inputs.setValue(4)
        layout.addRow("Number of Inputs:", self.mux_inputs)
        tab.setLayout(layout)
        return tab

    def create_decoder_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        self.dec_bits = QSpinBox()
        self.dec_bits.setRange(1, 4)
        self.dec_bits.setValue(2)
        layout.addRow("Address Bits:", self.dec_bits)
        tab.setLayout(layout)
        return tab

    def create_encoder_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        self.enc_lines = QSpinBox()
        self.enc_lines.setRange(2, 16)
        self.enc_lines.setValue(4)
        layout.addRow("Input Lines:", self.enc_lines)
        tab.setLayout(layout)
        return tab

    def create_demux_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        self.demux_sel = QSpinBox()
        self.demux_sel.setRange(1, 4)
        self.demux_sel.setValue(2)
        self.demux_out = QSpinBox()
        self.demux_out.setRange(2, 16)
        self.demux_out.setValue(4)
        layout.addRow("Select Bits:", self.demux_sel)
        layout.addRow("Output Lines:", self.demux_out)
        tab.setLayout(layout)
        return tab

    def create_shift_register_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        self.shift_length = QSpinBox()
        self.shift_length.setRange(1, 16)
        self.shift_length.setValue(4)
        self.shift_type = QComboBox()
        self.shift_type.addItems(["SIPO", "PISO"])
        layout.addRow("Register Length:", self.shift_length)
        layout.addRow("Type:", self.shift_type)
        tab.setLayout(layout)
        return tab

    def create_sram_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        self.sram_depth = QSpinBox()
        self.sram_depth.setRange(1, 64)
        self.sram_depth.setValue(16)
        self.sram_width = QSpinBox()
        self.sram_width.setRange(1, 16)
        self.sram_width.setValue(8)
        layout.addRow("Memory Depth:", self.sram_depth)
        layout.addRow("Data Width:", self.sram_width)
        tab.setLayout(layout)
        return tab

    def create_clock_divider_tab(self):
        tab = QWidget()
        layout = QFormLayout()
        self.clock_div = QSpinBox()
        self.clock_div.setRange(1, 64)
        self.clock_div.setValue(2)
        layout.addRow("Division Factor:", self.clock_div)
        tab.setLayout(layout)
        return tab

    def generate_code(self):
        entity = self.entity_name.text().strip() or "my_entity"
        arch = self.architecture_name.text().strip() or "behavioral"
        proc_type = self.proc_type.currentText().lower()
        component = self.tabs.tabText(self.tabs.currentIndex())
        
        code = ""
        
        if component == "MUX":
            code = self.generate_mux_code(entity, arch, proc_type)
        elif component == "Decoder":
            code = self.generate_decoder_code(entity, arch, proc_type)
        elif component == "Encoder":
            code = self.generate_encoder_code(entity, arch, proc_type)
        elif component == "Demux":
            code = self.generate_demux_code(entity, arch, proc_type)
        elif component == "Shift Register":
            code = self.generate_shift_register_code(entity, arch, proc_type)
        elif component == "SRAM":
            code = self.generate_sram_code(entity, arch, proc_type)
        elif component == "Clock Divider":
            code = self.generate_clock_divider_code(entity, arch, proc_type)
            
        self.code_display.setPlainText(code)

    def generate_mux_code(self, entity, arch, proc_type):
        n = self.mux_inputs.value()
        sel_bits = (n-1).bit_length()
        cases = []
        for i in range(n):
            bin_str = format(i, f"0{sel_bits}b")
            cases.append(f'            when "{bin_str}" => output <= inputs({i});')
        case_block = "\n".join(cases)
        
        return f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity {entity} is
    Port(
        inputs : in STD_LOGIC_VECTOR({n-1} downto 0);
        sel    : in STD_LOGIC_VECTOR({sel_bits-1} downto 0);
        output : out STD_LOGIC
    );
end {entity};

architecture {arch} of {entity} is
begin
    {proc_type} mux_{proc_type}(sel, inputs)
    begin
        case sel is
{case_block}
            when others => output <= '0';
        end case;
    end {proc_type};
end {arch};"""

    def generate_decoder_code(self, entity, arch, proc_type):
        bits = self.dec_bits.value()
        outputs = 2 ** bits
        cases = []
        for i in range(outputs):
            bin_str = format(i, f"0{bits}b")
            cases.append(f'            when "{bin_str}" => output <= (others => \'0\');')
            cases.append(f'            output({i}) <= \'1\';')
        case_block = "\n".join(cases)
        
        return f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity {entity} is
    Port(
        sel    : in STD_LOGIC_VECTOR({bits-1} downto 0);
        output : out STD_LOGIC_VECTOR({outputs-1} downto 0)
    );
end {entity};

architecture {arch} of {entity} is
begin
    {proc_type} decoder_{proc_type}(sel)
    begin
        output <= (others => '0');
        case sel is
{case_block}
        end case;
    end {proc_type};
end {arch};"""

    def generate_encoder_code(self, entity, arch, proc_type):
        lines = self.enc_lines.value()
        bits = (lines-1).bit_length()
        cases = []
        for i in range(lines):
            bin_str = format(1 << i, f"0{lines}b")
            cases.append(f'            when "{bin_str}" => output <= "{format(i, f"0{bits}b")}";')
        case_block = "\n".join(cases)
        
        return f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity {entity} is
    Port(
        input  : in STD_LOGIC_VECTOR({lines-1} downto 0);
        output : out STD_LOGIC_VECTOR({bits-1} downto 0)
    );
end {entity};

architecture {arch} of {entity} is
begin
    {proc_type} encoder_{proc_type}(input)
    begin
        case input is
{case_block}
            when others => output <= (others => '0');
        end case;
    end {proc_type};
end {arch};"""

    def generate_demux_code(self, entity, arch, proc_type):
        sel_bits = self.demux_sel.value()
        outputs = 2 ** sel_bits
        cases = []
        for i in range(outputs):
            bin_str = format(i, f"0{sel_bits}b")
            cases.append(f'            when "{bin_str}" => output({i}) <= input;')
        case_block = "\n".join(cases)
        
        return f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity {entity} is
    Port(
        input  : in STD_LOGIC;
        sel    : in STD_LOGIC_VECTOR({sel_bits-1} downto 0);
        output : out STD_LOGIC_VECTOR({outputs-1} downto 0)
    );
end {entity};

architecture {arch} of {entity} is
begin
    {proc_type} demux_{proc_type}(sel, input)
    begin
        output <= (others => '0');
        case sel is
{case_block}
        end case;
    end {proc_type};
end {arch};"""

    def generate_shift_register_code(self, entity, arch, proc_type):
        length = self.shift_length.value()
        reg_type = self.shift_type.currentText()
        
        if reg_type == "SIPO":
            return f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity {entity} is
    Port(
        clk     : in STD_LOGIC;
        reset   : in STD_LOGIC;
        data_in : in STD_LOGIC;
        data_out: out STD_LOGIC_VECTOR({length-1} downto 0)
    );
end {entity};

architecture {arch} of {entity} is
    signal reg : STD_LOGIC_VECTOR({length-1} downto 0);
begin
    process(clk, reset)
    begin
        if reset = '1' then
            reg <= (others => '0');
        elsif rising_edge(clk) then
            reg <= reg({length-2} downto 0) & data_in;
        end if;
    end process;
    data_out <= reg;
end {arch};"""
        else:  # PISO
            return f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity {entity} is
    Port(
        clk     : in STD_LOGIC;
        reset   : in STD_LOGIC;
        load    : in STD_LOGIC;
        data_in : in STD_LOGIC_VECTOR({length-1} downto 0);
        data_out: out STD_LOGIC
    );
end {entity};

architecture {arch} of {entity} is
    signal reg : STD_LOGIC_VECTOR({length-1} downto 0);
begin
    process(clk, reset)
    begin
        if reset = '1' then
            reg <= (others => '0');
        elsif rising_edge(clk) then
            if load = '1' then
                reg <= data_in;
            else
                reg <= reg({length-2} downto 0) & '0';
            end if;
        end if;
    end process;
    data_out <= reg({length-1});
end {arch};"""

    def generate_sram_code(self, entity, arch, proc_type):
        depth = self.sram_depth.value()
        width = self.sram_width.value()
        addr_bits = (depth-1).bit_length()
        
        return f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity {entity} is
    Port(
        clk      : in STD_LOGIC;
        we       : in STD_LOGIC;
        addr     : in STD_LOGIC_VECTOR({addr_bits-1} downto 0);
        data_in  : in STD_LOGIC_VECTOR({width-1} downto 0);
        data_out : out STD_LOGIC_VECTOR({width-1} downto 0)
    );
end {entity};

architecture {arch} of {entity} is
    type mem_type is array (0 to {depth-1}) of STD_LOGIC_VECTOR({width-1} downto 0);
    signal memory : mem_type := (others => (others => '0'));
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if we = '1' then
                memory(to_integer(unsigned(addr))) <= data_in;
            end if;
            data_out <= memory(to_integer(unsigned(addr)));
        end if;
    end process;
end {arch};"""

    def generate_clock_divider_code(self, entity, arch, proc_type):
        div = self.clock_div.value()
        return f"""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity {entity} is
    Port(
        clk_in  : in STD_LOGIC;
        clk_out : out STD_LOGIC
    );
end {entity};

architecture {arch} of {entity} is
    signal counter : integer range 0 to {div-1} := 0;
    signal clk_temp : STD_LOGIC := '0';
begin
    process(clk_in)
    begin
        if rising_edge(clk_in) then
            if counter = {div-1} then
                clk_temp <= not clk_temp;
                counter <= 0;
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;
    clk_out <= clk_temp;
end {arch};"""

    def copy_code(self):
        pyperclip.copy(self.code_display.toPlainText())
        self.status_bar.showMessage("Code copied to clipboard", 3000)

    def save_code(self):
        name = self.project_name.text().strip() or "vhdl_design"
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save VHDL Code", name, "VHDL Files (*.vhdl *.vhd)")
        if filename:
            with open(filename, 'w') as f:
                f.write(self.code_display.toPlainText())
            self.status_bar.showMessage(f"Saved: {filename}", 3000)

    def export_pdf(self):
        name = self.project_name.text().strip() or "vhdl_design"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", size=12)
        pdf.multi_cell(0, 10, self.code_display.toPlainText())
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", name, "PDF Files (*.pdf)")
        if filename:
            pdf.output(filename)
            self.status_bar.showMessage(f"Exported: {filename}", 3000)

    def create_menu(self):
        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("&File")
        exit_act = QAction("Exit", self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)
        
        help_menu = menu_bar.addMenu("&Help")
        about_act = QAction("About", self)
        about_act.triggered.connect(self.show_about)
        help_menu.addAction(about_act)
        
        self.setMenuBar(menu_bar)

    def show_about(self):
        QMessageBox.about(self, "About VHDL Generator",
            "VHDL Code Generator Pro\n\n"
            "Version 3.0\n"
            "All components working version\n"
            "© 2024 All rights reserved")

    def apply_theme(self):
        palette = QPalette()
        if self.dark_mode:
            palette.setColor(QPalette.Window, QColor(30, 30, 30))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(45, 45, 45))
            palette.setColor(QPalette.AlternateBase, QColor(37, 37, 38))
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(45, 45, 45))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.Highlight, QColor(86, 156, 214))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            palette = QApplication.style().standardPalette()
        
        self.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VHDLGeneratorApp()
    window.show()
    sys.exit(app.exec_())
