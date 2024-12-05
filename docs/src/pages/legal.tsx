import Layout from '@theme/Layout';


export default function Legal() {
    return (
        <>
            <Layout
                title={"Legal Notice"}
                description="Description will go into a meta tag in <head />">
                <main className='container padding--lg'>
                    <h1>Legal Notice</h1>
                    <h5>In accordance with § 5 of the German Telemedia Act (TMG)</h5>
                    <br />
                    <h3>Contact</h3>

                    {/* Contact - Name and Address */}
                    <h4 style={{ marginBottom: "0.5rem" }}>Name and Address</h4>
                    <ul style={
                        { listStyle: "none", padding: "0" }
                    }>
                        <li>Leo Gall</li>
                        <li>Föhrenweg 21</li>
                        <li>86926 Greifenberg</li>
                        <li>Germany</li>
                    </ul>

                    {/* Contact - E-Mail */}
                    <div className='margin-vert--md'>
                        <h4 style={{ marginBottom: "0.5rem" }}>E-Mail</h4>
                        <a href="mailto:daytistics@proton.me">daytistics@proton.me</a>
                    </div>

                    {/* Contact- Phone */}
                    <div className='margin-vert--md'>
                        <h4 style={{ marginBottom: "0.5rem" }}>Phone</h4>
                        <a href="tel:+491705915654">+49 170 591 5654</a>
                    </div>

                    <br />
                    <h3>Disclaimer</h3>
                    <div className='margin-vert--md'>
                        <h4 style={{ marginBottom: "0.5rem" }}>Accountability for Content</h4>
                        <p>
                            The contents of our pages have been created with the utmost care. However, we cannot guarantee the accuracy, completeness or topicality of our content. According to statutory provisions, we are furthermore responsible for our own content on these web pages. In this matter, please note that we are not obliged to monitor the transmitted or saved information of third parties, or investigate circumstances pointing to illegal activity. Our obligations to remove or block the use of information under generally applicable laws remain unaffected by this as per §§ 8 to 10 of the Telemedia Act (TMG).
                        </p>
                    </div>

                    <div className='margin-vert--md'>
                        <h4 style={{ marginBottom: "0.5rem" }}>Accountability for Links</h4>
                        <p>
                            Responsibility for the content of external links (to web pages of third parties) lies solely with the operators of the linked pages. No violations were evident to us at the time of linking. Should any legal infringement become known to us, we will remove the respective link immediately.                        </p>
                    </div>
                </main>
            </Layout>
        </>
    )
}