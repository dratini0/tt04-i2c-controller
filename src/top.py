#!/usr/bin/env python3

from amaranth import *
from amaranth.back import verilog

class I2CControllerTop(Elaboratable):
    """The top level, responsible for pinout definition"""

    def __init__(self):
        self.ui_in = Signal(8)
        self.uo_out = Signal(8)
        self.uio_in = Signal(8)
        self.uio_out = Signal(8)
        self.uio_oe = Signal(8)
        self.ena = Signal(1)
        self.clk = Signal(1)
        self.rst_n = Signal(1)

    def elaborate(self, platform):
        m = Module()

        # Set up clock domain from io_in[0]
        cd_sync = ClockDomain("sync")
        m.d.comb += cd_sync.clk.eq(self.clk)
        m.d.comb += cd_sync.rst.eq(~self.rst_n)
        m.domains += cd_sync

        m.d.comb += [
            self.uo_out.eq(~self.ui_in),
            self.uio_out.eq(0),
            self.uio_oe.eq(self.ui_in),
        ]

        return m

    def get_ports(self):
        return [
            self.ui_in,
            self.uo_out,
            self.uio_in,
            self.uio_out,
            self.uio_oe,
            self.ena,
            self.clk,
            self.rst_n
        ]


if __name__ == "__main__":
    top = I2CControllerTop()
    print(
        verilog.convert(
            top,
            ports=top.get_ports(),
            name="tt_um_dratini0_i2c",
            emit_src=False,
            strip_internal_attrs=True,
        )
    )
