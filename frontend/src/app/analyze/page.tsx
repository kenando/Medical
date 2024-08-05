import styles from "./page.module.css";
import {InputForm} from "@/app/analyze/input";
import {Header} from "@/components/header/header";
import {Navbar} from "@/components/nav-bar/nav-bar";

export default async function AnalyzePage() {
    return (
        <div className={styles.main}>
            <Header/>
            <div className={styles.content}>
                <Navbar/>
                <InputForm/>
            </div>
        </div>
    )
}
