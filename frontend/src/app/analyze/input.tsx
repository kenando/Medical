"use client"
import React, { useState } from 'react';
import { Group, rem, Text, MultiSelect, Button } from '@mantine/core';
import { IconPhoto, IconUpload, IconX } from '@tabler/icons-react';
import { Dropzone } from '@mantine/dropzone';
import { Loading } from "@/components/loading/loading";

const KEYPOINTS_NAMES = [
    { value: "nose", label: "鼻" },
    { value: "eye(L)", label: "左目" },
    { value: "eye(R)", label: "右目" },
    { value: "ear(L)", label: "左耳" },
    { value: "ear(R)", label: "右耳" },
    { value: "shoulder(L)", label: "左肩" },
    { value: "shoulder(R)", label: "右肩" },
    { value: "elbow(L)", label: "左肘" },
    { value: "elbow(R)", label: "右肘" },
    { value: "wrist(L)", label: "左手首" },
    { value: "wrist(R)", label: "右手首" },
    { value: "hip(L)", label: "左腰" },
    { value: "hip(R)", label: "右腰" },
    { value: "knee(L)", label: "左膝" },
    { value: "knee(R)", label: "右膝" },
    { value: "ankle(L)", label: "左足首" },
    { value: "ankle(R)", label: "右足首" },
];

export function InputForm() {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [selectedKeypoints, setSelectedKeypoints] = useState<string[]>([]);

    const handleFileChange = (files: File[]) => {
        setFile(files[0]);
    };

    const handleSubmit = async () => {
        if (!file) {
            console.error('No file selected');
            return;
        }
        const formData = new FormData();
        formData.append('video', file);
        formData.append('keypoints', JSON.stringify(selectedKeypoints));
        setLoading(true);
        const response = await fetch('http://localhost:5000/video', {
            method: 'POST',
            body: formData,
        });
        setLoading(false);
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'output.mp4';
            document.body.appendChild(link);
            link.click();
            link.remove();
        } else {
            console.error('Failed to upload file');
        }
    };

    return (
        <div>
            <Loading visible={loading} />
            <Dropzone
                onDrop={(files) => handleFileChange(files)}
                onReject={(files) => console.log('rejected files', files)}
                maxSize={50 * 1024 ** 2}
                accept={["video/*"]}
            >
                <Group justify="center" gap="xl" mih={220} style={{ pointerEvents: 'none' }}>
                    <Dropzone.Accept>
                        <IconUpload
                            style={{ width: rem(52), height: rem(52), color: 'var(--mantine-color-blue-6)' }}
                            stroke={1.5}
                        />
                    </Dropzone.Accept>
                    <Dropzone.Reject>
                        <IconX
                            style={{ width: rem(52), height: rem(52), color: 'var(--mantine-color-red-6)' }}
                            stroke={1.5}
                        />
                    </Dropzone.Reject>
                    <Dropzone.Idle>
                        <IconPhoto
                            style={{ width: rem(52), height: rem(52), color: 'var(--mantine-color-dimmed)' }}
                            stroke={1.5}
                        />
                    </Dropzone.Idle>

                    <div>
                        <Text size="xl" inline>
                            動画をここにドラッグするか、クリックしてファイルを選択
                        </Text>
                        <Text size="sm" c="dimmed" inline mt={7}>
                            最大ファイルサイズは50MBです
                        </Text>
                    </div>
                </Group>
                {file && (
                    <Text size="lg" inline mt={7}>
                        選択されたファイル: {file.name}
                    </Text>
                )}
            </Dropzone>
            <MultiSelect
                label="キーポイント"
                placeholder="キーポイントを選択"
                data={KEYPOINTS_NAMES}
                searchable
                nothingFound="オプションなし"
                value={selectedKeypoints}
                onChange={setSelectedKeypoints}
                clearable
            />
            <Button onClick={handleSubmit}>送信</Button>
        </div>
    );
}
