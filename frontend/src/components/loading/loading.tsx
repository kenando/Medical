import { LoadingOverlay, Skeleton } from "@mantine/core"
import React from "react"
import styles from "@/components/loading/loading.module.css"

export function Loading({ visible }: { visible: boolean }) {
  return <LoadingOverlay visible={visible} zIndex={1000} overlayProps={{ radius: "sm", blur: 2 }} />
}

export function LoadingSkeleton({ height }: { height: number }) {
  return (
    <div className={styles.main}>
      <Skeleton height={height} mt={20} radius="sm" />
    </div>
  )
}
