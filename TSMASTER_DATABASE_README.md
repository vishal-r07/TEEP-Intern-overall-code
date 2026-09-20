# STM32F103 J1939 Database for TSMaster

Use `STM32F103_J1939_Signal_Generator.dbc` with the code in this same folder.  It contains only the 17 PGNs that `j1939_arduino_generator.ino` transmits, with the byte positions, scaling, offsets, priorities, and source addresses used by the firmware.

## TSMaster setup

1. Connect the TSMaster CAN interface to the MCP2551 CAN bus: CAN_H to CAN_H, CAN_L to CAN_L, and a common ground.
2. Terminate the two ends of the bus with 120 ohms.  Do not add a third terminator in the middle.
3. In the TSMaster hardware/channel configuration, select **CAN**, **Classic CAN**, and **250 kbit/s**.  The Arduino `j1939_can_helper.cpp` configures the Nucleo CAN peripheral for 250 kbit/s, not 500 kbit/s.
4. Load the DBC through the database configuration/import area, then start measurement and open Trace or Graphics.
5. Filter/display extended frames.  The main engine ECU uses source address `0x00`; the transmission messages use source address `0x03`.

## Expected frames

You should see 29-bit IDs such as `0CF00400` (EEC1 / engine speed), `0CFEF100` (CCVS1 / vehicle speed), `0CF00503` (ETC2 / transmission gear), and `0CFEF803` (transmission fluids).  The DBC stores the normal DBC extended-ID representation, so TSMaster should match and decode these raw Trace IDs automatically.

## Important scope

The older databases in `TEEP_intern_Arthitha` are useful J1939 references, but they are not a safe direct choice for this firmware: several contain other source addresses or signal layouts.  This database is intentionally tied to `j1939_arduino_generator.ino` and `j1939_signal_definitions.c`.

If Trace shows raw frames but no decoded signals after importing this file, first verify the channel is 250 kbit/s and the Trace view is showing extended frames.
