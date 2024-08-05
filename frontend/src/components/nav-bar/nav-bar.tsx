"use client"
import { Box, Collapse, Group, rem, ScrollArea, ThemeIcon, UnstyledButton } from "@mantine/core"
import { IconChevronRight, IconUser } from "@tabler/icons-react"
import styles from "@/components/nav-bar/nav-bar.module.css"
import React, { useState } from "react"
import Link from "next/link"

type NavItems = {
  label: string
  icon: React.FC
  links?: {
    label: string
    link: string
  }[]
  initialOpened?: boolean
}

function navItem(): NavItems[] {
  return [
    {
      label: "動作解析",
      icon: IconUser,
      links: [
        {
          label: `解析`,
          link: `/analyze`,
        },
      ],
      initialOpened: true,
    },
  ]
}

export function Navbar() {
  const items = navItem()
  const links = items
    .map((item) => {
      return <LinksGroup {...item} key={item.label} />
    })
  return (
    <nav className={styles.nav}>
      <ScrollArea className={styles.scroll}>
        <div className={styles.inner}>{links}</div>
      </ScrollArea>
    </nav>
  )
}

interface LinksGroupProps {
  initialOpened?: boolean
  links?: { label: string; link: string }[]
  label: string
  icon: React.FC<React.SVGProps<SVGSVGElement>>
}

function LinksGroup({ links, initialOpened, icon: Icon, label, session }: LinksGroupProps) {
  const hasLinks = Array.isArray(links)
  const [opened, setOpened] = useState(initialOpened || false)
  const items = (hasLinks ? links : [])?.map((link) => {
    return (
      <Link className={styles.link} href={link.link} key={link.label}>
        {link.label}
      </Link>
    )
  })

  return (
    <UnstyledButton className={styles.control}>
      <Group>
        <Box className={styles.label}>
          <ThemeIcon variant="light" size={24}>
            <Icon style={{ width: rem(18), height: rem(18) }} />
          </ThemeIcon>
          <Box
            ml="md"
            onClick={() => {
              setOpened((o) => !o)
            }}
          >
            {label}
          </Box>
          {hasLinks && (
            <IconChevronRight
              stroke={1.5}
              onClick={() => {
                setOpened((o) => !o)
              }}
              style={{
                width: rem(16),
                height: rem(16),
                transform: opened ? "rotate(-90deg)" : "none",
              }}
            />
          )}
        </Box>
        {hasLinks ? <Collapse in={opened}>{items}</Collapse> : null}
      </Group>
    </UnstyledButton>
  )
}
