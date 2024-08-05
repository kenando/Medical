"use client"
import { Button, Menu, MenuItem } from "@mantine/core"
import classes from "@/components/header/header.module.css"
import Link from "next/link"

export function Header() {

  return (
    <header className={classes.header}>
      <div className={classes.inner}>
        <Link href={`/analyze`} className={classes.title}>
          山梨大学MA
        </Link>
      </div>
    </header>
  )
}
