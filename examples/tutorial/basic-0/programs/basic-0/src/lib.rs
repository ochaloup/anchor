use anchor_lang::prelude::*;

declare_id!("7RJ7c3E3rxFD3NScPVssfKk5psBVXEWjQBwPdex2DACE");

#[program]
mod basic_0 {
    use super::*;
    pub fn initialize(_ctx: Context<Initialize>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}
